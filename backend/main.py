from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import re
import logging

from partsbox import get_part_location

# Load .env environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Get API key
API_KEY = os.getenv("PARTSBOX_API_KEY", "")

# Initialize FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper to extract part ID from URL or raw input
def extract_part_id(url_or_id: str) -> str:
    # If it's already a raw 26-character ID
    if re.fullmatch(r"[a-z0-9]{26}", url_or_id):
        return url_or_id

    # Try to extract from full PartsBox URL
    match = re.search(r"https?://partsbox\.com/[^/]+/parts/([a-z0-9]{26})", url_or_id)
    if match:
        return match.group(1)

    raise ValueError("Invalid PartsBox part URL or ID format")

# API route
@app.post("/get-location")
async def get_location(url: str = Form(...)):
    try:
        logger.info(f"Received POST /get-location with url: {url}")
        part_path = extract_part_id(url)
        logger.info(f"Parsed part path: {part_path}")
        location = await get_part_location(part_path, API_KEY)
        logger.info(f"Resolved location: {location}")
        return {"location": location}
    except Exception as e:
        logger.exception("Error resolving location")
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Mount built frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

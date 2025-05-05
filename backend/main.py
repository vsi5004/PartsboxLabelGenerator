from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse
from dotenv import load_dotenv
import httpx
import os
import re
import json
import logging

from partsbox import get_part_location

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Get API key
API_KEY = os.getenv("PARTSBOX_API_KEY", "")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_part_id(url_or_id: str) -> str:
    if re.fullmatch(r"[a-z0-9]{26}", url_or_id):
        return url_or_id
    match = re.search(r"https?://partsbox\.com/[^/]+/parts/([a-z0-9]{26})", url_or_id)
    if match:
        return match.group(1)
    raise ValueError("Invalid PartsBox part URL or ID format")


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


@app.get("/stream-labels")
async def stream_labels():
    async def event_generator():
        headers = {
            "Authorization": f"APIKey {API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.partsbox.com/api/1/part/all",
                headers=headers,
                json={}
            )
            resp.raise_for_status()
            parts = resp.json().get("data", [])

            total = len(parts)
            sent = 0

            for part in parts:
                part_id = part.get("part/id")
                if not part_id:
                    continue

                location = await get_part_location(part_id, API_KEY)
                if location.lower() in ["no location found", "no storage id"]:
                    continue

                url = f"https://partsbox.com/parts/{part_id}"
                label = {"url": url, "location": location}
                sent += 1

                yield {
                    "event": "label",
                    "data": json.dumps(label),
                }

                yield {
                    "event": "progress",
                    "data": json.dumps({"current": sent, "total": total}),
                }

        yield {
            "event": "done",
            "data": json.dumps({"status": "complete", "count": sent}),
        }

    return EventSourceResponse(event_generator())


app.mount("/", StaticFiles(directory="static", html=True), name="static")

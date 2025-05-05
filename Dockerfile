# Base image for backend
FROM python:3.12-slim as backend

WORKDIR /app
COPY backend/ /app/
RUN pip install --no-cache-dir -r requirements.txt

# Base image for frontend
FROM node:23-slim as frontend

WORKDIR /app
COPY frontend/ /app/
RUN npm install && npm run build

# Final stage: Serve frontend + backend
FROM python:3.12-slim

# Backend
WORKDIR /app
COPY --from=backend /app /app
COPY --from=frontend /app/dist /app/static

# Install deps again
RUN pip install --no-cache-dir -r requirements.txt

# Uvicorn + static mount
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

"""Configuration for the OFDS Demonstration API."""

from pathlib import Path
import os

# Repo root (parent of api/); overridable for deployments where data lives elsewhere.
DATA_ROOT = Path(os.environ.get("DATA_ROOT", Path(__file__).resolve().parent.parent))

API_PREFIX = "/api/v1"

# Less common than 8000/8080; nginx is the public entry point.
UVICORN_HOST = os.environ.get("UVICORN_HOST", "127.0.0.1")
UVICORN_PORT = int(os.environ.get("UVICORN_PORT", "8742"))

# Directories under DATA_ROOT that are not country data folders.
SKIP_DIRS = frozenset({".git", ".github", "api", "tippecanoe", "__pycache__", ".venv", "venv"})

CORS_ORIGINS = [
    "https://ofds-demo.opentelecomdata.org",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

# Optional admin reload endpoint (set ENABLE_ADMIN_RELOAD=1 to enable).
ENABLE_ADMIN_RELOAD = os.environ.get("ENABLE_ADMIN_RELOAD", "").lower() in (
    "1",
    "true",
    "yes",
)

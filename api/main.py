"""OFDS Demonstration API — FastAPI application."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .catalog import Catalog
from .config import (
    API_PREFIX,
    CORS_ORIGINS,
    ENABLE_ADMIN_RELOAD,
    UVICORN_HOST,
    UVICORN_PORT,
)

catalog = Catalog()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    catalog.reload()
    yield


app = FastAPI(
    title="OFDS Demonstration API",
    description=(
        "Catalog and serve Open Fibre Data Standard (OFDS) JSON datasets "
        "from the OFDS-public-data repository."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get(f"{API_PREFIX}/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "networks": len(catalog.list_all()),
    }


@app.get(f"{API_PREFIX}/catalog")
def get_catalog() -> list[dict[str, Any]]:
    return [e.to_catalog_dict() for e in catalog.list_all()]


@app.get(f"{API_PREFIX}/countries")
def get_countries() -> list[str]:
    return catalog.list_countries()


@app.get(f"{API_PREFIX}/countries/{{country}}/operators")
def get_operators(country: str) -> list[str]:
    operators = catalog.list_operators(country)
    if operators is None:
        raise HTTPException(status_code=404, detail=f"Country not found: {country}")
    return operators


@app.get(f"{API_PREFIX}/networks/{{country}}/{{operator}}")
def get_network(country: str, operator: str) -> dict[str, Any]:
    entry = catalog.get(country, operator)
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"Network not found: {country}/{operator}",
        )
    return entry.to_metadata_dict()


@app.get(f"{API_PREFIX}/networks/{{country}}/{{operator}}/ofds-json")
def get_ofds_json(country: str, operator: str) -> FileResponse:
    entry = catalog.get(country, operator)
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"Network not found: {country}/{operator}",
        )
    path = entry.ofds_json_path
    if not path.is_file():
        raise HTTPException(
            status_code=404,
            detail=f"OFDS JSON file missing for {country}/{operator}",
        )
    return FileResponse(
        path,
        media_type="application/json",
        filename=path.name,
    )


if ENABLE_ADMIN_RELOAD:

    @app.post(f"{API_PREFIX}/admin/reload")
    def admin_reload() -> dict[str, Any]:
        count = catalog.reload()
        return {"reloaded": True, "networks": count}


def main() -> None:
    import uvicorn

    uvicorn.run(
        "api.main:app",
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=False,
    )


if __name__ == "__main__":
    main()

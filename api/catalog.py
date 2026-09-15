"""Directory walker and lightweight OFDS metadata extraction."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config import API_PREFIX, DATA_ROOT, SKIP_DIRS


@dataclass
class NetworkEntry:
    country: str
    operator: str
    network_name: str
    network_id: str | None
    schema_href: str | None
    node_count: int
    span_count: int
    ofds_json_path: Path
    ofds_json_url: str = field(init=False)

    def __post_init__(self) -> None:
        self.ofds_json_url = (
            f"{API_PREFIX}/networks/{self.country}/{self.operator}/ofds-json"
        )

    def to_catalog_dict(self) -> dict[str, Any]:
        return {
            "country": self.country,
            "operator": self.operator,
            "network_name": self.network_name,
            "network_id": self.network_id,
            "schema_href": self.schema_href,
            "node_count": self.node_count,
            "span_count": self.span_count,
            "ofds_json": self.ofds_json_url,
        }

    def to_metadata_dict(self) -> dict[str, Any]:
        return {
            **self.to_catalog_dict(),
            "file_name": self.ofds_json_path.name,
            "file_size_bytes": self.ofds_json_path.stat().st_size,
        }


class Catalog:
    """In-memory index of OFDS networks discovered under DATA_ROOT."""

    def __init__(self, data_root: Path | None = None) -> None:
        self.data_root = data_root or DATA_ROOT
        self._entries: list[NetworkEntry] = []
        self._by_key: dict[tuple[str, str], NetworkEntry] = {}
        self.reload()

    def reload(self) -> int:
        entries: list[NetworkEntry] = []
        by_key: dict[tuple[str, str], NetworkEntry] = {}

        for country_dir in sorted(self.data_root.iterdir()):
            if not country_dir.is_dir() or country_dir.name.startswith("."):
                continue
            if country_dir.name in SKIP_DIRS:
                continue

            for operator_dir in sorted(country_dir.iterdir()):
                if not operator_dir.is_dir() or operator_dir.name.startswith("."):
                    continue

                json_files = sorted(operator_dir.glob("*ofds-json*.json"))
                if not json_files:
                    continue

                ofds_path = json_files[0]
                entry = _extract_metadata(
                    country=country_dir.name,
                    operator=operator_dir.name,
                    ofds_path=ofds_path,
                )
                if entry is None:
                    continue

                key = (entry.country, entry.operator)
                entries.append(entry)
                by_key[key] = entry

        self._entries = entries
        self._by_key = by_key
        return len(entries)

    def list_all(self) -> list[NetworkEntry]:
        return list(self._entries)

    def list_countries(self) -> list[str]:
        return sorted({e.country for e in self._entries})

    def list_operators(self, country: str) -> list[str] | None:
        operators = [e.operator for e in self._entries if e.country == country]
        if not operators:
            # Distinguish unknown country from empty: check if country dir exists
            country_dir = self.data_root / country
            if country_dir.is_dir() and country not in SKIP_DIRS:
                return []
            return None
        return operators

    def get(self, country: str, operator: str) -> NetworkEntry | None:
        return self._by_key.get((country, operator))


def _extract_metadata(
    country: str, operator: str, ofds_path: Path
) -> NetworkEntry | None:
    """Parse OFDS JSON for name, schema link, and node/span counts."""
    try:
        with ofds_path.open(encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None

    networks = data.get("networks") or []
    if not networks:
        return NetworkEntry(
            country=country,
            operator=operator,
            network_name=operator,
            network_id=None,
            schema_href=None,
            node_count=0,
            span_count=0,
            ofds_json_path=ofds_path,
        )

    network = networks[0]
    schema_href = None
    for link in network.get("links") or []:
        if link.get("rel") == "describedby" and link.get("href"):
            schema_href = link["href"]
            break

    return NetworkEntry(
        country=country,
        operator=operator,
        network_name=network.get("name") or operator,
        network_id=network.get("id"),
        schema_href=schema_href,
        node_count=len(network.get("nodes") or []),
        span_count=len(network.get("spans") or []),
        ofds_json_path=ofds_path,
    )

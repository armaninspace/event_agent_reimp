"""Reference data snapshot hashing for reproducibility audits."""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path


REFERENCE_SNAPSHOT_FILES = (
    "joined_city_week_game_economic.csv",
    "joined_msa_week_game_economic.csv",
)


def build_reference_snapshot(reference_dir: Path) -> dict[str, object]:
    """Return hashes and basic shape metadata for reference CSV files."""
    files = []
    for filename in REFERENCE_SNAPSHOT_FILES:
        path = reference_dir / filename
        files.append(
            {
                "path": str(path),
                "sha256": _sha256(path),
                "byte_count": path.stat().st_size,
                "row_count": _csv_row_count(path),
            }
        )
    return {
        "schema_version": "phase-020.reference-data-snapshot.v1",
        "algorithm": "sha256",
        "file_count": len(files),
        "files": files,
        "combined_sha256": _combined_hash(files),
    }


def snapshot_is_complete(snapshot: object) -> bool:
    """Return whether a snapshot contains all required file metadata."""
    if not isinstance(snapshot, dict):
        return False
    files = snapshot.get("files")
    if not isinstance(files, list) or len(files) != len(REFERENCE_SNAPSHOT_FILES):
        return False
    required = {"path", "sha256", "byte_count", "row_count"}
    return all(isinstance(item, dict) and required <= item.keys() for item in files)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        return sum(1 for _ in reader)


def _combined_hash(files: list[dict[str, object]]) -> str:
    digest = hashlib.sha256()
    for item in files:
        digest.update(str(item["path"]).encode("utf-8"))
        digest.update(str(item["sha256"]).encode("utf-8"))
    return digest.hexdigest()

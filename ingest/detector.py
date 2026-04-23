"""MIME type detection from magic bytes + filename extension."""
from __future__ import annotations

import os

_MAGIC: list[tuple[bytes, str]] = [
    (b"%PDF", "application/pdf"),
    (b"\xd0\xcf\x11\xe0", "application/msword"),
    (b"PK\x03\x04", "application/zip"),
]

_EXT_MIME: dict[str, str] = {
    ".pdf":  "application/pdf",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls":  "application/vnd.ms-excel",
    ".csv":  "text/csv",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc":  "application/msword",
    ".txt":  "text/plain",
    ".html": "text/html",
    ".htm":  "text/html",
}


def detect_mime(data: bytes, filename: str = "") -> str:
    """Detect MIME type -- magic bytes first, filename extension as fallback."""
    for magic, mime in _MAGIC:
        if data[: len(magic)] == magic:
            if mime == "application/zip" and filename:
                return _EXT_MIME.get(_ext(filename), mime)
            return mime
    if filename:
        return _EXT_MIME.get(_ext(filename), "application/octet-stream")
    return "application/octet-stream"


def _ext(filename: str) -> str:
    _, ext = os.path.splitext(filename.lower())
    return ext

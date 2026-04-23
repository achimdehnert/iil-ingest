"""CSV extractor (stdlib only -- no extra dependency)."""
from __future__ import annotations

import csv
import io

from ingest.types import ExtractedContent

SUPPORTED_MIMES: frozenset[str] = frozenset({"text/csv", "text/plain"})


class CSVExtractor:
    """Extract rows from CSV bytes using stdlib csv."""

    supported_mimes = SUPPORTED_MIMES

    def can_handle(self, mime_type: str) -> bool:
        return mime_type in self.supported_mimes

    def extract(self, data: bytes) -> ExtractedContent:
        errors: list[str] = []
        rows: list[list[str]] = []

        try:
            text = data.decode("utf-8-sig", errors="replace")
            rows = list(csv.reader(io.StringIO(text)))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"CSV read error: {exc}")
            text = data.decode("utf-8-sig", errors="replace")

        return ExtractedContent(
            raw_bytes=data,
            text="\n".join(",".join(r) for r in rows),
            tables=[rows] if rows else [],
            metadata={"row_count": len(rows), "col_count": len(rows[0]) if rows else 0},
            mime_type="text/csv",
            page_count=1,
            extraction_errors=errors,
        )

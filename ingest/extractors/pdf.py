"""PDF extractor using pdfplumber."""
from __future__ import annotations

from ingest.types import ExtractedContent

SUPPORTED_MIMES: frozenset[str] = frozenset({"application/pdf"})


class PDFExtractor:
    """Extract text, tables and metadata from PDF bytes (requires pdfplumber)."""

    supported_mimes = SUPPORTED_MIMES

    def can_handle(self, mime_type: str) -> bool:
        return mime_type in self.supported_mimes

    def extract(self, data: bytes) -> ExtractedContent:
        try:
            import pdfplumber  # type: ignore[import]
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "pdfplumber required. Install with: pip install iil-ingest[pdf]"
            ) from exc

        import io

        text_parts: list[str] = []
        tables: list[list[list[str]]] = []
        errors: list[str] = []
        meta: dict = {}

        try:
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                meta = {
                    "title":   pdf.metadata.get("Title", ""),
                    "author":  pdf.metadata.get("Author", ""),
                    "creator": pdf.metadata.get("Creator", ""),
                    "pages":   len(pdf.pages),
                }
                for i, page in enumerate(pdf.pages):
                    try:
                        text_parts.append(page.extract_text() or "")
                        for tbl in page.extract_tables() or []:
                            tables.append(
                                [[str(cell or "") for cell in row] for row in tbl]
                            )
                    except Exception as exc:  # noqa: BLE001
                        errors.append(f"Page {i}: {exc}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"PDF open error: {exc}")

        return ExtractedContent(
            raw_bytes=data,
            text="\n".join(text_parts),
            tables=tables,
            metadata=meta,
            mime_type="application/pdf",
            page_count=meta.get("pages", 0),
            extraction_errors=errors,
        )

"""PDF extractor using pdfplumber with optional Tesseract OCR fallback."""
from __future__ import annotations

from ingest.types import ExtractedContent

SUPPORTED_MIMES: frozenset[str] = frozenset({"application/pdf"})


class PDFExtractor:
    """Extract text, tables and metadata from PDF bytes.

    Args:
        ocr_fallback: When ``True`` and pdfplumber yields no text (scanned PDF),
            fall back to Tesseract OCR via ``iil-ingest[ocr]``.
    """

    supported_mimes = SUPPORTED_MIMES

    def __init__(self, *, ocr_fallback: bool = False) -> None:
        self.ocr_fallback = ocr_fallback

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

        text = "\n".join(text_parts)

        if not text.strip() and self.ocr_fallback:
            from ingest.extractors.ocr import ocr_pdf_bytes

            ocr_text = ocr_pdf_bytes(data)
            if ocr_text.strip():
                text = ocr_text
                meta["ocr_used"] = True

        return ExtractedContent(
            raw_bytes=data,
            text=text,
            tables=tables,
            metadata=meta,
            mime_type="application/pdf",
            page_count=meta.get("pages", 0),
            extraction_errors=errors,
        )

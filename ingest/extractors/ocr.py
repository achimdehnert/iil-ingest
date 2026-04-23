"""OCR-based text extraction from PDF bytes via Tesseract.

Requires the [ocr] extra:
    pip install iil-ingest[ocr]

System dependencies (must be installed separately):
    apt install tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng poppler-utils
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def ocr_pdf_bytes(data: bytes, lang: str = "deu+eng") -> str:
    """Extract text from PDF bytes via Tesseract OCR.

    Converts each PDF page to an image (via pdf2image/poppler),
    then runs pytesseract. Returns concatenated text of all pages.

    Args:
        data:  Raw PDF bytes.
        lang:  Tesseract language string, e.g. ``"deu+eng"`` (default).

    Returns:
        Extracted text, or empty string on failure.

    Raises:
        ImportError: If pytesseract or pdf2image are not installed.
    """
    try:
        import pytesseract  # type: ignore[import]
        from pdf2image import convert_from_bytes  # type: ignore[import]
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "OCR requires: pip install iil-ingest[ocr]\n"
            "System deps: apt install tesseract-ocr tesseract-ocr-deu poppler-utils"
        ) from exc

    try:
        images = convert_from_bytes(data, dpi=200)
    except Exception as exc:  # noqa: BLE001
        logger.warning("pdf2image conversion failed: %s", exc)
        return ""

    text_parts: list[str] = []
    for i, image in enumerate(images):
        try:
            page_text = pytesseract.image_to_string(image, lang=lang)
            if page_text.strip():
                text_parts.append(page_text)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Tesseract failed on page %d: %s", i, exc)

    return "\n".join(text_parts)

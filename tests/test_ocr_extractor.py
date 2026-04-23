"""Tests for OCR extractor and PDFExtractor.ocr_fallback."""
from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock, patch

from ingest.extractors.pdf import PDFExtractor


def _make_pdf2image_mock(images: list) -> ModuleType:
    """Return a minimal pdf2image stub."""
    mod = MagicMock(spec=ModuleType)
    mod.convert_from_bytes = MagicMock(return_value=images)
    return mod


def _make_pytesseract_mock(side_effects) -> ModuleType:
    """Return a minimal pytesseract stub."""
    mod = MagicMock(spec=ModuleType)
    if isinstance(side_effects, list):
        mod.image_to_string = MagicMock(side_effect=side_effects)
    else:
        mod.image_to_string = MagicMock(return_value=side_effects)
    return mod


# ── PDFExtractor: ocr_fallback disabled (default) ────────────────────────────

def test_pdf_extractor_default_no_ocr():
    """ocr_fallback defaults to False."""
    extractor = PDFExtractor()
    assert extractor.ocr_fallback is False


def test_pdf_extractor_ocr_fallback_flag():
    """ocr_fallback=True is stored."""
    extractor = PDFExtractor(ocr_fallback=True)
    assert extractor.ocr_fallback is True


# ── PDFExtractor: OCR not called when pdfplumber returns text ─────────────────

def test_pdf_extractor_no_ocr_when_text_present():
    """If pdfplumber returns text, OCR must NOT be triggered."""
    page_mock = MagicMock()
    page_mock.extract_text.return_value = "Sicherheitsdatenblatt"
    page_mock.extract_tables.return_value = []

    pdf_mock = MagicMock()
    pdf_mock.__enter__ = lambda s: pdf_mock
    pdf_mock.__exit__ = MagicMock(return_value=False)
    pdf_mock.pages = [page_mock]
    pdf_mock.metadata = {}

    with patch("pdfplumber.open", return_value=pdf_mock):
        with patch("ingest.extractors.ocr.ocr_pdf_bytes") as ocr_mock:
            result = PDFExtractor(ocr_fallback=True).extract(b"%PDF-fake")

    ocr_mock.assert_not_called()
    assert "Sicherheitsdatenblatt" in result.text


# ── PDFExtractor: OCR triggered when pdfplumber returns empty text ─────────────

def test_pdf_extractor_ocr_fallback_triggered():
    """If pdfplumber returns empty text and ocr_fallback=True, OCR is called."""
    page_mock = MagicMock()
    page_mock.extract_text.return_value = ""
    page_mock.extract_tables.return_value = []

    pdf_mock = MagicMock()
    pdf_mock.__enter__ = lambda s: pdf_mock
    pdf_mock.__exit__ = MagicMock(return_value=False)
    pdf_mock.pages = [page_mock]
    pdf_mock.metadata = {}

    with patch("pdfplumber.open", return_value=pdf_mock):
        with patch(
            "ingest.extractors.ocr.ocr_pdf_bytes",
            return_value="Aceton H225 H319 P210",
        ) as ocr_mock:
            result = PDFExtractor(ocr_fallback=True).extract(b"%PDF-scanned")

    ocr_mock.assert_called_once_with(b"%PDF-scanned")
    assert result.text == "Aceton H225 H319 P210"
    assert result.metadata.get("ocr_used") is True


def test_pdf_extractor_ocr_not_called_when_fallback_disabled():
    """ocr_fallback=False: OCR must NOT be called even if pdfplumber yields empty."""
    page_mock = MagicMock()
    page_mock.extract_text.return_value = ""
    page_mock.extract_tables.return_value = []

    pdf_mock = MagicMock()
    pdf_mock.__enter__ = lambda s: pdf_mock
    pdf_mock.__exit__ = MagicMock(return_value=False)
    pdf_mock.pages = [page_mock]
    pdf_mock.metadata = {}

    with patch("pdfplumber.open", return_value=pdf_mock):
        with patch("ingest.extractors.ocr.ocr_pdf_bytes") as ocr_mock:
            result = PDFExtractor(ocr_fallback=False).extract(b"%PDF-empty")

    ocr_mock.assert_not_called()
    assert result.text == ""
    assert not result.metadata.get("ocr_used")


# ── ocr_pdf_bytes: unit tests (sys.modules mocks — no system install needed) ──

def test_ocr_pdf_bytes_returns_text():
    """ocr_pdf_bytes returns joined page texts from pytesseract."""
    fake_image = MagicMock()
    p2i = _make_pdf2image_mock([fake_image, fake_image])
    tess = _make_pytesseract_mock(["Seite 1", "Seite 2"])

    with patch.dict(sys.modules, {"pdf2image": p2i, "pytesseract": tess}):
        from ingest.extractors import ocr as ocr_mod
        import importlib
        importlib.reload(ocr_mod)
        result = ocr_mod.ocr_pdf_bytes(b"fake-pdf")

    assert result == "Seite 1\nSeite 2"


def test_ocr_pdf_bytes_skips_empty_pages():
    """Pages with only whitespace are excluded from result."""
    fake_image = MagicMock()
    p2i = _make_pdf2image_mock([fake_image, fake_image])
    tess = _make_pytesseract_mock(["  \n  ", "Inhalt"])

    with patch.dict(sys.modules, {"pdf2image": p2i, "pytesseract": tess}):
        from ingest.extractors import ocr as ocr_mod
        import importlib
        importlib.reload(ocr_mod)
        result = ocr_mod.ocr_pdf_bytes(b"fake-pdf")

    assert result == "Inhalt"


def test_ocr_pdf_bytes_returns_empty_on_conversion_error():
    """If pdf2image fails, ocr_pdf_bytes returns empty string (no exception)."""
    p2i = MagicMock(spec=ModuleType)
    p2i.convert_from_bytes = MagicMock(side_effect=Exception("poppler not found"))
    tess = MagicMock(spec=ModuleType)

    with patch.dict(sys.modules, {"pdf2image": p2i, "pytesseract": tess}):
        from ingest.extractors import ocr as ocr_mod
        import importlib
        importlib.reload(ocr_mod)
        result = ocr_mod.ocr_pdf_bytes(b"bad-pdf")

    assert result == ""


def test_ocr_pdf_bytes_custom_lang():
    """lang parameter is forwarded to pytesseract."""
    fake_image = MagicMock()
    p2i = _make_pdf2image_mock([fake_image])
    tess = _make_pytesseract_mock("text")

    with patch.dict(sys.modules, {"pdf2image": p2i, "pytesseract": tess}):
        from ingest.extractors import ocr as ocr_mod
        import importlib
        importlib.reload(ocr_mod)
        ocr_mod.ocr_pdf_bytes(b"pdf", lang="eng")

    tess.image_to_string.assert_called_once_with(fake_image, lang="eng")

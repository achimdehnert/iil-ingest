"""Tests for optional-dependency extractors (pdfplumber, openpyxl in dev deps)."""
from __future__ import annotations

import io

import pytest

# ---------------------------------------------------------------------------
# Excel extractor (openpyxl is in dev deps)
# ---------------------------------------------------------------------------

def _make_xlsx(rows: list[list]) -> bytes:
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    for row in rows:
        ws.append(row)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_excel_can_handle():
    from ingest.extractors.excel import ExcelExtractor
    ext = ExcelExtractor()
    assert ext.can_handle("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert not ext.can_handle("text/csv")


def test_excel_basic_extraction():
    from ingest.extractors.excel import ExcelExtractor
    data = _make_xlsx([["Rechnung", "Nr", "001"], ["MwSt.", "19%", ""]])
    result = ExcelExtractor().extract(data)
    assert "Rechnung" in result.text
    assert result.page_count == 1
    assert len(result.tables) == 1
    assert result.tables[0][0] == ["Rechnung", "Nr", "001"]


def test_excel_metadata_sheet_names():
    from ingest.extractors.excel import ExcelExtractor
    data = _make_xlsx([["col1", "col2"]])
    result = ExcelExtractor().extract(data)
    assert "sheet_names" in result.metadata
    assert len(result.metadata["sheet_names"]) == 1


def test_excel_corrupt_data():
    from ingest.extractors.excel import ExcelExtractor
    result = ExcelExtractor().extract(b"not an excel file")
    assert len(result.extraction_errors) > 0


# ---------------------------------------------------------------------------
# PDF extractor (pdfplumber is in dev deps)
# ---------------------------------------------------------------------------

def test_pdf_can_handle():
    from ingest.extractors.pdf import PDFExtractor
    ext = PDFExtractor()
    assert ext.can_handle("application/pdf")
    assert not ext.can_handle("text/csv")


def test_pdf_corrupt_returns_error():
    from ingest.extractors.pdf import PDFExtractor
    result = PDFExtractor().extract(b"not a real pdf")
    assert len(result.extraction_errors) > 0
    assert result.mime_type == "application/pdf"
    assert result.text == ""


def test_pdf_extract_returns_extracted_content():
    from ingest.extractors.pdf import PDFExtractor
    from ingest.types import ExtractedContent
    result = PDFExtractor().extract(b"%PDF-invalid")
    assert isinstance(result, ExtractedContent)


# ---------------------------------------------------------------------------
# DOCX extractor — can_handle only (python-docx not in dev deps)
# ---------------------------------------------------------------------------

def test_docx_can_handle():
    from ingest.extractors.docx import DOCXExtractor
    ext = DOCXExtractor()
    assert ext.can_handle(
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert not ext.can_handle("application/pdf")


def test_docx_missing_dep_raises():
    """If python-docx is not installed, extract() must raise ImportError."""
    import sys
    import unittest.mock as mock

    from ingest.extractors.docx import DOCXExtractor

    with mock.patch.dict(sys.modules, {"docx": None}):
        with pytest.raises((ImportError, TypeError)):
            DOCXExtractor().extract(b"data")

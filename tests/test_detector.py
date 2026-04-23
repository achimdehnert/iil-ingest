"""Tests for ingest.detector."""
from ingest.detector import detect_mime


def test_detect_pdf_magic():
    assert detect_mime(b"%PDF-1.4 rest") == "application/pdf"


def test_detect_pdf_by_extension():
    assert detect_mime(b"notmagic", "document.pdf") == "application/pdf"


def test_detect_csv_by_extension():
    assert detect_mime(b"a,b,c", "data.csv") == "text/csv"


def test_detect_xlsx_zip_magic_with_extension():
    data = b"PK\x03\x04" + b"\x00" * 100
    assert detect_mime(data, "report.xlsx") == (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


def test_detect_docx_zip_magic_with_extension():
    data = b"PK\x03\x04" + b"\x00" * 100
    assert detect_mime(data, "report.docx") == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


def test_detect_fallback_unknown():
    assert detect_mime(b"random bytes") == "application/octet-stream"


def test_detect_txt_extension():
    assert detect_mime(b"hello world", "note.txt") == "text/plain"


def test_detect_zip_no_filename():
    data = b"PK\x03\x04" + b"\x00" * 10
    assert detect_mime(data) == "application/zip"

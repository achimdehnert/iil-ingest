"""Tests for CSVExtractor."""
from ingest.extractors.csv import CSVExtractor


def test_csv_basic():
    data = b"name,age\nAlice,30\nBob,25"
    result = CSVExtractor().extract(data)
    assert result.mime_type == "text/csv"
    assert "Alice" in result.text
    assert result.metadata["row_count"] == 3


def test_csv_can_handle():
    ext = CSVExtractor()
    assert ext.can_handle("text/csv")
    assert not ext.can_handle("application/pdf")


def test_csv_tables_structure():
    result = CSVExtractor().extract(b"a,b\n1,2")
    assert len(result.tables) == 1
    assert result.tables[0][0] == ["a", "b"]


def test_csv_empty():
    result = CSVExtractor().extract(b"")
    assert result.text == ""
    assert result.metadata["row_count"] == 0


def test_csv_utf8_bom():
    data = b"\xef\xbb\xbfname,value\ntest,42"
    result = CSVExtractor().extract(data)
    assert "name" in result.text

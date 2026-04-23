"""Tests for ingest.types."""
from ingest.types import ClassificationResult, ExtractedContent, IngestedDocument


def test_extracted_content_defaults():
    ec = ExtractedContent(raw_bytes=b"hello", text="hello")
    assert ec.tables == []
    assert ec.metadata == {}
    assert ec.mime_type == ""
    assert ec.page_count == 0
    assert ec.extraction_errors == []


def test_extracted_content_with_values():
    ec = ExtractedContent(
        raw_bytes=b"data", text="some text", mime_type="application/pdf", page_count=3
    )
    assert ec.page_count == 3
    assert ec.mime_type == "application/pdf"


def test_classification_result_defaults():
    cr = ClassificationResult(doc_type="RECHNUNG", confidence="HIGH", score=42.0)
    assert cr.matched_profiles == []


def test_ingested_document_defaults():
    ec = ExtractedContent(raw_bytes=b"", text="")
    doc = IngestedDocument(
        source_name="test.pdf", content=ec, doc_type="KONTOAUSZUG",
        confidence="MEDIUM", score=18.0,
    )
    assert doc.extra == {}
    assert doc.matched_profiles == []


def test_ingested_document_extra():
    ec = ExtractedContent(raw_bytes=b"", text="")
    doc = IngestedDocument(
        source_name="r.pdf", content=ec, doc_type="RECHNUNG",
        confidence="HIGH", score=50.0, extra={"amount": "99.00"},
    )
    assert doc.extra["amount"] == "99.00"

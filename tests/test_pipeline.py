"""Tests for IngestPipeline."""
from dataclasses import dataclass

from ingest.classifier import ProfileClassifier
from ingest.extractors.csv import CSVExtractor
from ingest.pipeline import IngestPipeline
from ingest.types import IngestedDocument


@dataclass
class _InvoiceProfile:
    name = "RECHNUNG"
    patterns = [(r"\brechnung\b", 10), (r"rechnungsnummer", 8)]
    min_score = 10


def test_pipeline_csv_classify():
    data = b"Rechnung,Rechnungsnummer,2026-001\nMwSt.,19%,0.00"
    pipeline = IngestPipeline(
        extractors=[CSVExtractor()],
        classifier=ProfileClassifier([_InvoiceProfile()]),
    )
    doc = pipeline.run(data, filename="test.csv")
    assert doc.doc_type == "RECHNUNG"
    assert doc.source_name == "test.csv"
    assert doc.content.mime_type == "text/csv"


def test_pipeline_no_classifier():
    pipeline = IngestPipeline(extractors=[CSVExtractor()])
    doc = pipeline.run(b"a,b,c", filename="data.csv")
    assert doc.doc_type == "UNKNOWN"
    assert doc.confidence == "UNKNOWN"


def test_pipeline_no_extractor_fallback():
    pipeline = IngestPipeline(extractors=[])
    doc = pipeline.run(b"hello world", filename="notes.txt")
    assert "No extractor" in doc.content.extraction_errors[0]
    assert "hello world" in doc.content.text


def test_pipeline_returns_ingested_document():
    pipeline = IngestPipeline(extractors=[CSVExtractor()])
    doc = pipeline.run(b"col1,col2", filename="data.csv")
    assert isinstance(doc, IngestedDocument)


def test_pipeline_source_name_preserved():
    pipeline = IngestPipeline(extractors=[CSVExtractor()])
    doc = pipeline.run(b"x", filename="myfile.csv")
    assert doc.source_name == "myfile.csv"

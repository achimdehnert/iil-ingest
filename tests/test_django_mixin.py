"""Tests for ingest.django.mixins.IngestMixin."""
from __future__ import annotations

import io

from ingest.django.mixins import IngestMixin
from ingest.extractors.csv import CSVExtractor
from ingest.pipeline import IngestPipeline


class _FakeModel(IngestMixin):
    """Minimal fake model with a file field and ingest_result store."""

    def __init__(self, data: bytes, filename: str = "test.csv"):
        file_obj = io.BytesIO(data)
        file_obj.name = filename
        self.file = file_obj
        self.ingest_result: dict = {}


def _pipeline():
    return IngestPipeline(extractors=[CSVExtractor()])


def test_ingest_file_returns_ingested_document():
    from ingest.types import IngestedDocument
    model = _FakeModel(b"a,b\n1,2")
    result = model.ingest_file(_pipeline())
    assert isinstance(result, IngestedDocument)


def test_ingest_file_stores_result():
    model = _FakeModel(b"Rechnung,Nummer\n2026,001", "r.csv")
    model.ingest_file(_pipeline())
    assert "doc_type" in model.ingest_result
    assert "confidence" in model.ingest_result
    assert "score" in model.ingest_result
    assert "matched_profiles" in model.ingest_result


def test_ingest_file_custom_field():
    model = _FakeModel(b"x,y")
    model.other = model.file
    del model.file
    result = model.ingest_file(_pipeline(), file_field="other")
    assert result is not None


def test_ingest_file_no_ingest_result_field():
    """Models without ingest_result field should still work."""

    class _Minimal(IngestMixin):
        def __init__(self):
            f = io.BytesIO(b"a,b")
            f.name = "data.csv"
            self.file = f

    result = _Minimal().ingest_file(_pipeline())
    assert result.source_name == "data.csv"

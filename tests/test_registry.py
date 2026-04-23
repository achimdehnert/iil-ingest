"""Tests for IngestRegistry."""
from dataclasses import dataclass

from ingest.extractors.csv import CSVExtractor
from ingest.registry import IngestRegistry


@dataclass
class _SimpleProfile:
    name = "TEST"
    patterns = [(r"test", 10)]
    min_score = 5


def test_register_extractor():
    reg = IngestRegistry()
    reg.register_extractor(CSVExtractor())
    assert len(reg.extractors) == 1


def test_register_profile_and_classify():
    reg = IngestRegistry()
    reg.register_profile(_SimpleProfile())
    clf = reg.build_classifier()
    assert clf.classify("this is a test").doc_type == "TEST"


def test_registry_repr():
    reg = IngestRegistry()
    reg.register_extractor(CSVExtractor())
    assert "CSVExtractor" in repr(reg)


def test_extractors_returns_copy():
    reg = IngestRegistry()
    reg.register_extractor(CSVExtractor())
    lst = reg.extractors
    lst.clear()
    assert len(reg.extractors) == 1


def test_empty_registry():
    reg = IngestRegistry()
    assert reg.extractors == []
    clf = reg.build_classifier()
    assert clf.classify("anything").confidence == "UNKNOWN"

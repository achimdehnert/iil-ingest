"""Tests for ingest.classifier.ProfileClassifier."""
from dataclasses import dataclass

import pytest

from ingest.classifier import ProfileClassifier


@dataclass
class _InvoiceProfile:
    name = "RECHNUNG"
    patterns = [(r"\brechnung\b", 10), (r"rechnungsnummer", 8), (r"mwst\.", 6)]
    min_score = 10


@dataclass
class _ContractProfile:
    name = "VERTRAG"
    patterns = [(r"\bvertrag\b", 10), (r"vertragspartner", 8), (r"k.ndigungsfrist", 6)]
    min_score = 10


@pytest.fixture
def classifier():
    return ProfileClassifier([_InvoiceProfile(), _ContractProfile()])


def test_classify_high_confidence(classifier):
    text = "Rechnung Rechnungsnummer 2026-001 MwSt. 19% Rechnung Rechnung"
    result = classifier.classify(text)
    assert result.doc_type == "RECHNUNG"
    assert result.confidence == "HIGH"
    assert result.score >= 30


def test_classify_medium_confidence(classifier):
    result = classifier.classify("Rechnungsnummer 2026-001")
    assert result.doc_type == "RECHNUNG"
    assert result.confidence in ("MEDIUM", "LOW")


def test_classify_selects_best_match(classifier):
    text = "Vertrag Vertragspartner Kundigungsfrist Rechnung"
    assert classifier.classify(text).doc_type == "VERTRAG"


def test_classify_empty_returns_unknown(classifier):
    result = classifier.classify("")
    assert result.doc_type == "SONSTIGES"
    assert result.confidence == "UNKNOWN"


def test_classify_whitespace_returns_unknown(classifier):
    assert classifier.classify("   \n  ").confidence == "UNKNOWN"


def test_classify_no_match_returns_unknown(classifier):
    assert classifier.classify("lorem ipsum dolor sit amet").confidence == "UNKNOWN"


def test_matched_profiles_populated(classifier):
    result = classifier.classify("Rechnung Rechnungsnummer MwSt.")
    assert len(result.matched_profiles) > 0


def test_custom_thresholds():
    clf = ProfileClassifier([_InvoiceProfile()], high_threshold=5, medium_threshold=2)
    assert clf.classify("Rechnung").confidence == "HIGH"

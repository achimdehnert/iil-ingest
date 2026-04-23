"""Tests for german_hr profiles."""
from ingest.classifier import ProfileClassifier
from ingest.profiles.german_hr import GERMAN_HR_PROFILES


def _clf():
    return ProfileClassifier(GERMAN_HR_PROFILES)


def test_profiles_count():
    assert len(GERMAN_HR_PROFILES) >= 10


def test_classify_rechnung():
    text = "Rechnung Rechnungsnummer 2026-042 MwSt. 19% Netto Brutto zahlungsziel"
    assert _clf().classify(text).doc_type == "RECHNUNG"


def test_classify_kontoauszug():
    text = "Kontoauszug IBAN DE12 3456 Buchungsdatum Kontostand Haben Soll BIC"
    assert _clf().classify(text).doc_type == "KONTOAUSZUG"


def test_classify_arbeitsvertrag():
    text = "Arbeitsvertrag Arbeitgeber Arbeitnehmer Bruttogehalt Kundigungsfrist"
    assert _clf().classify(text).doc_type == "ARBEITSVERTRAG"


def test_classify_gehaltsabrechnung():
    text = "Lohnabrechnung Bruttogehalt Nettogehalt Lohnsteuer Sozialversicherung Steuerklasse"
    assert _clf().classify(text).doc_type == "GEHALTSABRECHNUNG"


def test_classify_lebenslauf():
    text = "Lebenslauf Berufserfahrung Schulausbildung Kenntnisse Referenzen"
    assert _clf().classify(text).doc_type == "LEBENSLAUF"


def test_classify_unknown():
    assert _clf().classify("the quick brown fox").confidence == "UNKNOWN"


def test_profile_names_unique():
    names = [p.name for p in GERMAN_HR_PROFILES]
    assert len(names) == len(set(names))


def test_all_profiles_have_patterns():
    for p in GERMAN_HR_PROFILES:
        assert len(p.patterns) >= 3, f"{p.name} needs >= 3 patterns"

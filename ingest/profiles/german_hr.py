"""German HR document classification profiles (migrated from dms-hub)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class _Profile:
    name: str
    patterns: list[tuple[str, int]]
    min_score: int = 10


GERMAN_HR_PROFILES: list[_Profile] = [
    _Profile(
        name="PERSONALAUSWEIS",
        patterns=[
            (r"personalausweis", 10),
            (r"ausweisnummer", 8),
            (r"bundesrepublik\s+deutschland", 5),
            (r"g.ltig\s+bis", 4),
            (r"geburtsort", 4),
            (r"staatsangeh.rigkeit", 4),
        ],
    ),
    _Profile(
        name="REISEPASS",
        patterns=[
            (r"reisepass", 10),
            (r"passport", 8),
            (r"passnummer", 8),
            (r"pass-nr", 6),
        ],
    ),
    _Profile(
        name="KONTOAUSZUG",
        patterns=[
            (r"kontoauszug", 10),
            (r"iban", 8),
            (r"kontonummer", 8),
            (r"buchungsdatum", 6),
            (r"\bhaben\b", 4),
            (r"\bsoll\b", 4),
            (r"kontostand", 6),
            (r"bic\b", 4),
        ],
    ),
    _Profile(
        name="MIETVERTRAG",
        patterns=[
            (r"mietvertrag", 10),
            (r"\bmiete\b", 6),
            (r"vermieter", 8),
            (r"\bmieter\b", 8),
            (r"kaltmiete", 8),
            (r"nebenkosten", 6),
            (r"kaution", 6),
            (r"k.ndigungsfrist", 5),
        ],
    ),
    _Profile(
        name="ARBEITSVERTRAG",
        patterns=[
            (r"arbeitsvertrag", 10),
            (r"arbeitgeber", 8),
            (r"arbeitnehmer", 8),
            (r"\bgehalt\b", 6),
            (r"bruttogehalt", 8),
            (r"k.ndigungsfrist", 6),
            (r"probezeit", 5),
        ],
    ),
    _Profile(
        name="GEHALTSABRECHNUNG",
        patterns=[
            (r"gehaltsabrechnung|lohnabrechnung", 10),
            (r"bruttolohn|bruttogehalt", 8),
            (r"nettolohn|nettogehalt", 8),
            (r"sozialversicherung", 6),
            (r"lohnsteuer", 6),
            (r"steuerklasse", 6),
            (r"rentenversicherung", 5),
        ],
    ),
    _Profile(
        name="KRANKENVERSICHERUNG",
        patterns=[
            (r"krankenversicherung", 10),
            (r"versicherungsnummer", 8),
            (r"mitgliedsbescheinigung", 8),
            (r"krankenkasse", 8),
            (r"gesetzliche\s+krankenversicherung", 6),
        ],
    ),
    _Profile(
        name="STEUERBESCHEID",
        patterns=[
            (r"steuerbescheid", 10),
            (r"einkommensteuerbescheid", 10),
            (r"zu versteuerndes einkommen", 8),
            (r"finanzamt", 6),
            (r"steuernummer", 6),
            (r"veranlagungszeitraum", 5),
        ],
    ),
    _Profile(
        name="LEBENSLAUF",
        patterns=[
            (r"lebenslauf", 10),
            (r"curriculum vitae|\bcv\b", 8),
            (r"berufserfahrung", 8),
            (r"schulausbildung|ausbildung", 6),
            (r"kenntnisse", 5),
            (r"referenzen", 4),
        ],
    ),
    _Profile(
        name="RECHNUNG",
        patterns=[
            (r"\brechnung\b", 10),
            (r"rechnungsnummer", 8),
            (r"rechnungsdatum", 8),
            (r"mehrwertsteuer|mwst\.|ust\.", 6),
            (r"zahlungsziel", 6),
            (r"\bnetto\b", 4),
            (r"\bbrutto\b", 4),
            (r"lieferschein", 4),
        ],
    ),
]

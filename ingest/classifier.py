"""Domain-agnostic keyword-profile classifier."""
from __future__ import annotations

import re
from typing import Protocol, runtime_checkable

from ingest.types import ClassificationResult

_CONFIDENCE_HIGH = 30
_CONFIDENCE_MEDIUM = 15

_UNKNOWN = ClassificationResult(
    doc_type="SONSTIGES",
    confidence="UNKNOWN",
    score=0.0,
    matched_profiles=[],
)


@runtime_checkable
class ClassifierProfile(Protocol):
    """Protocol for document classification profiles."""

    name: str
    patterns: list[tuple[str, int]]
    min_score: int


class ProfileClassifier:
    """Domain-agnostic keyword-profile classifier (migrated from dms-hub)."""

    def __init__(
        self,
        profiles: list[ClassifierProfile],
        high_threshold: int = _CONFIDENCE_HIGH,
        medium_threshold: int = _CONFIDENCE_MEDIUM,
    ) -> None:
        self._profiles = profiles
        self._high = high_threshold
        self._medium = medium_threshold

    def classify(self, text: str) -> ClassificationResult:
        if not text or not text.strip():
            return _UNKNOWN

        text_lower = text.lower()
        scores: dict[str, float] = {}
        matched: dict[str, list[str]] = {}

        for profile in self._profiles:
            score = 0.0
            hits: list[str] = []
            for pattern, weight in profile.patterns:
                found = re.findall(pattern, text_lower)
                if found:
                    score += weight * min(len(found), 3)
                    hits.append(pattern)
            scores[profile.name] = score
            if hits:
                matched[profile.name] = hits

        if not scores or max(scores.values()) == 0:
            return _UNKNOWN

        best = max(scores, key=scores.__getitem__)
        best_score = scores[best]

        if best_score >= self._high:
            confidence: str = "HIGH"
        elif best_score >= self._medium:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        return ClassificationResult(
            doc_type=best,
            confidence=confidence,  # type: ignore[arg-type]
            score=best_score,
            matched_profiles=matched.get(best, []),
        )

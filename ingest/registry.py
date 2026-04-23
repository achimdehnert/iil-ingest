"""Central registry for extractors and classifier profiles."""
from __future__ import annotations

from ingest.classifier import ClassifierProfile, ProfileClassifier
from ingest.extractors.base import ExtractorProtocol


class IngestRegistry:
    """Collects extractors and profiles; builds pipeline components."""

    def __init__(self) -> None:
        self._extractors: list[ExtractorProtocol] = []
        self._profiles: list[ClassifierProfile] = []

    def register_extractor(self, extractor: ExtractorProtocol) -> None:
        self._extractors.append(extractor)

    def register_profile(self, profile: ClassifierProfile) -> None:
        self._profiles.append(profile)

    @property
    def extractors(self) -> list[ExtractorProtocol]:
        return list(self._extractors)

    def build_classifier(self) -> ProfileClassifier:
        return ProfileClassifier(self._profiles)

    def __repr__(self) -> str:
        return (
            f"IngestRegistry("
            f"extractors={[type(e).__name__ for e in self._extractors]}, "
            f"profiles={[p.name for p in self._profiles]})"
        )

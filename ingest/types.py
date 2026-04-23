"""Core data types for iil-ingest."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Confidence = Literal["HIGH", "MEDIUM", "LOW", "UNKNOWN"]


@dataclass
class ExtractedContent:
    """Raw extraction result from an extractor."""

    raw_bytes: bytes
    text: str
    tables: list[list[list[str]]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    mime_type: str = ""
    page_count: int = 0
    extraction_errors: list[str] = field(default_factory=list)


@dataclass
class ClassificationResult:
    """Result from ProfileClassifier.classify()."""

    doc_type: str
    confidence: Confidence
    score: float
    matched_profiles: list[str] = field(default_factory=list)


@dataclass
class IngestedDocument:
    """Final output of IngestPipeline.run()."""

    source_name: str
    content: ExtractedContent
    doc_type: str
    confidence: Confidence
    score: float
    matched_profiles: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

"""iil-ingest -- Reusable Document Ingestion Package (ADR-170)."""
from __future__ import annotations

from ingest.classifier import ProfileClassifier
from ingest.pipeline import IngestPipeline
from ingest.registry import IngestRegistry
from ingest.types import ClassificationResult, ExtractedContent, IngestedDocument

__version__ = "0.1.0"
__all__ = [
    "IngestPipeline",
    "ProfileClassifier",
    "IngestRegistry",
    "ExtractedContent",
    "IngestedDocument",
    "ClassificationResult",
]

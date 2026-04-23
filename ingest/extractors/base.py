"""ExtractorProtocol -- base interface for all extractors."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from ingest.types import ExtractedContent


@runtime_checkable
class ExtractorProtocol(Protocol):
    """Extract structured content from raw bytes."""

    supported_mimes: frozenset[str]

    def extract(self, data: bytes) -> ExtractedContent: ...

    def can_handle(self, mime_type: str) -> bool: ...

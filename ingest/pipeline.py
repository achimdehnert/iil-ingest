"""IngestPipeline: detect -> extract -> classify."""
from __future__ import annotations

from ingest.classifier import ProfileClassifier
from ingest.detector import detect_mime
from ingest.extractors.base import ExtractorProtocol
from ingest.types import ExtractedContent, IngestedDocument


class IngestPipeline:
    """Orchestrates: detect MIME -> extract content -> classify document."""

    def __init__(
        self,
        extractors: list[ExtractorProtocol],
        classifier: ProfileClassifier | None = None,
    ) -> None:
        self._extractors = extractors
        self._classifier = classifier

    def run(self, data: bytes, filename: str = "") -> IngestedDocument:
        """Run the full ingestion pipeline on raw bytes."""
        mime_type = detect_mime(data, filename)
        content = self._extract(data, mime_type)

        if self._classifier is not None:
            result = self._classifier.classify(content.text)
            doc_type = result.doc_type
            confidence = result.confidence
            score = result.score
            matched = result.matched_profiles
        else:
            doc_type = "UNKNOWN"
            confidence = "UNKNOWN"
            score = 0.0
            matched = []

        return IngestedDocument(
            source_name=filename,
            content=content,
            doc_type=doc_type,
            confidence=confidence,  # type: ignore[arg-type]
            score=score,
            matched_profiles=matched,
        )

    def _extract(self, data: bytes, mime_type: str) -> ExtractedContent:
        for extractor in self._extractors:
            if extractor.can_handle(mime_type):
                return extractor.extract(data)
        return ExtractedContent(
            raw_bytes=data,
            text=data.decode("utf-8", errors="replace"),
            mime_type=mime_type,
            extraction_errors=[f"No extractor for mime_type={mime_type!r}"],
        )

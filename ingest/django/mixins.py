"""Django integration mixin for iil-ingest."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ingest.types import IngestedDocument


class IngestMixin:
    """Mixin for Django models with a FileField.

    Adds ingest_file() that runs IngestPipeline on self.file
    and stores doc_type + confidence in self.ingest_result.

    Usage::

        class MyDocument(IngestMixin, models.Model):
            file = models.FileField(...)
            ingest_result = models.JSONField(default=dict)

        doc_obj.ingest_file(pipeline=my_pipeline)
    """

    def ingest_file(self, pipeline: Any, file_field: str = "file") -> "IngestedDocument":
        file_obj = getattr(self, file_field)
        data = file_obj.read()
        filename = getattr(file_obj, "name", "")
        result = pipeline.run(data, filename=filename)
        if hasattr(self, "ingest_result"):
            self.ingest_result = {
                "doc_type": result.doc_type,
                "confidence": result.confidence,
                "score": result.score,
                "matched_profiles": result.matched_profiles,
            }
        return result

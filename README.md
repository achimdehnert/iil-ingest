# iil-ingest

> Reusable Document Ingestion Package for the IIL Platform — **ADR-170**

**Pattern:** iil-enrichment (ADR-169) — Pure Python Core, Protocol-based, optional Django integration

## Installation

```bash
pip install iil-ingest[pdf]        # PDF only
pip install iil-ingest[all]        # PDF + Excel + DOCX
pip install iil-ingest[all,django] # + Django mixins
```

## Quick Start

```python
from ingest import IngestPipeline, ProfileClassifier
from ingest.extractors.pdf import PDFExtractor
from ingest.profiles.german_hr import GERMAN_HR_PROFILES

pipeline = IngestPipeline(
    extractors=[PDFExtractor()],
    classifier=ProfileClassifier(GERMAN_HR_PROFILES),
)

with open("rechnung.pdf", "rb") as f:
    doc = pipeline.run(f.read(), filename="rechnung.pdf")

print(doc.doc_type)    # "RECHNUNG"
print(doc.confidence)  # "HIGH"
print(doc.score)       # 42.0
```

## Custom Profile

```python
from dataclasses import dataclass
from ingest import IngestPipeline, ProfileClassifier
from ingest.extractors.pdf import PDFExtractor

@dataclass
class SdsProfile:
    name = "SDS"
    patterns = [
        (r"sicherheitsdatenblatt", 10),
        (r"gefahrenhinweis|h\d{3}", 8),
        (r"reach", 6),
    ]
    min_score = 10

pipeline = IngestPipeline(
    extractors=[PDFExtractor()],
    classifier=ProfileClassifier([SdsProfile()]),
)
```

## Architecture

```
Upload -> iil-ingest (detect + extract + classify)
       -> iil-enrichment (optional enrichment)
       -> Django DB / Paperless (archive)
```

## Supported Formats

| Format | Extra | Extractor |
|--------|-------|-----------|
| PDF | `[pdf]` | `PDFExtractor` (pdfplumber) |
| Excel (.xlsx) | `[excel]` | `ExcelExtractor` (openpyxl) |
| CSV | -- | `CSVExtractor` (stdlib) |
| DOCX | `[docx]` | `DOCXExtractor` (python-docx) |

## Pipeline Flow

```
bytes + filename
  -> detect_mime()          # magic bytes + extension
  -> extractor.extract()    # text, tables, metadata
  -> classifier.classify()  # doc_type, confidence, score
  -> IngestedDocument
```

## References

- ADR-170: `platform/docs/adr/ADR-170-iil-ingest-document-ingestion-package.md`
- Pattern: iil-enrichment (ADR-169)
- Migrated from: `dms-hub/apps/benefits/classifier.py`, `dms-hub/apps/accounting/extractor.py`

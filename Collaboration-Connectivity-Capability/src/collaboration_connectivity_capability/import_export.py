"""JSON, JSONL, CSV, and TEXT import/export with schema and transformation checks."""

from __future__ import annotations

import csv
import io
import json
from typing import Any

from .models import ExportRequest, ExportResult, ImportRequest, ImportResult
from .transformation import transform_record

FORMATS = frozenset({"JSON", "JSONL", "CSV", "TEXT"})


def _validate_schema(record: Any, schema: dict[str, type | tuple[type, ...]] | None) -> None:
    if schema is None:
        return
    if not isinstance(record, dict):
        raise ValueError("schema validation requires object records")
    for field_name, expected_type in schema.items():
        if field_name not in record:
            raise ValueError(f"missing required field: {field_name}")
        if not isinstance(record[field_name], expected_type):
            raise ValueError(f"invalid type for field: {field_name}")


def import_data(request: ImportRequest) -> ImportResult:
    format_name = request.format.upper()
    if format_name not in FORMATS:
        return ImportResult(False, errors=(f"unsupported format: {request.format}",))
    text = request.content.decode("utf-8") if isinstance(request.content, bytes) else request.content
    try:
        if format_name == "JSON":
            decoded = json.loads(text)
            records = decoded if isinstance(decoded, list) else [decoded]
        elif format_name == "JSONL":
            records = [json.loads(line) for line in text.splitlines() if line.strip()]
        elif format_name == "CSV":
            records = list(csv.DictReader(io.StringIO(text)))
        else:
            records = [line for line in text.splitlines()]
    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
        return ImportResult(False, errors=(f"invalid {format_name}: {exc}",))

    accepted: list[Any] = []
    errors: list[str] = []
    for index, record in enumerate(records):
        try:
            _validate_schema(record, request.schema)
            if request.transformation_rules:
                if not isinstance(record, dict):
                    raise ValueError("transformation requires object records")
                transformed = transform_record(record, request.transformation_rules)
                if not transformed.success:
                    raise ValueError(transformed.errors[0])
                record = transformed.data
            accepted.append(record)
        except (TypeError, ValueError) as exc:
            errors.append(f"record {index}: {exc}")
    return ImportResult(not errors, tuple(accepted), len(records), len(errors), tuple(errors))


def export_data(request: ExportRequest) -> ExportResult:
    format_name = request.format.upper()
    if format_name not in FORMATS:
        return ExportResult(False, errors=(f"unsupported format: {request.format}",))
    records: list[Any] = []
    try:
        for record in request.records:
            _validate_schema(record, request.schema)
            if request.transformation_rules:
                if not isinstance(record, dict):
                    raise ValueError("transformation requires object records")
                transformed = transform_record(record, request.transformation_rules)
                if not transformed.success:
                    raise ValueError(transformed.errors[0])
                record = transformed.data
            records.append(record)
        if format_name == "JSON":
            content = json.dumps(records, ensure_ascii=False)
        elif format_name == "JSONL":
            content = "\n".join(json.dumps(item, ensure_ascii=False) for item in records)
        elif format_name == "CSV":
            if records and not all(isinstance(item, dict) for item in records):
                raise ValueError("CSV export requires object records")
            buffer = io.StringIO()
            fieldnames = list(dict.fromkeys(key for item in records for key in item))
            writer = csv.DictWriter(buffer, fieldnames=fieldnames)
            if fieldnames: writer.writeheader(); writer.writerows(records)
            content = buffer.getvalue()
        else:
            content = "\n".join(str(item) for item in records)
        return ExportResult(True, content, len(records))
    except (TypeError, ValueError, csv.Error) as exc:
        return ExportResult(False, errors=(str(exc),))

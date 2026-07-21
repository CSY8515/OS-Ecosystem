# Import / Export Contract

Version: v1.0.0

## Formats

The supported formats are JSON, JSONL, CSV, and UTF-8 text. Format names are case-insensitive. Malformed input returns an `ImportResult` with errors and does not raise raw parser exceptions.

## Import

`ImportRequest` contains content, format, an optional field/type schema, and optional transformation rules. `ImportResult` reports success, accepted records, processed count, failure count, and per-record errors. Partial validation failures retain valid records and explicitly report the rejected positions.

## Export

`ExportRequest` contains records, format, an optional schema, and transformation rules. `ExportResult` contains encoded text, exported count, and errors. CSV requires object records.

## Transformation

The mechanical operations are rename/map, include, exclude, default, type conversion, and metadata mapping. Transformations cannot execute code or contain project business rules. The source project owns canonical schemas and semantic validation.

## Security

Import/export content is never automatically persisted or copied into execution records. Size limits and access authorization belong at the Safety and application boundary.

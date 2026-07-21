# Project Integration Contract

Version: v1.0.0

Projects may depend only on names exported by `enhancement_capability`. Every request identifies `source`, `target`, `action`, and a dictionary payload. Callers must inspect `success` and `error_code`, avoid secrets or unapproved personal data, and retain authority over downstream changes.

Components expose a unique ID and action, validate inputs and outputs, return dictionary results, and provide health information. Direct access to another project's storage or runtime is prohibited.

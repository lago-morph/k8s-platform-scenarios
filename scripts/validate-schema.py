#!/usr/bin/env python3
"""Validate a JSON document against a JSON Schema (draft 2020-12).

Used by scripts/lint-json; also runnable standalone:

    python3 scripts/validate-schema.py SCHEMA_FILE DOCUMENT_FILE

Exit status: 0 = valid, 1 = validation errors, 2 = tooling/usage error.
Dependency: the `jsonschema` package (pip install jsonschema).
"""
import json
import sys


def main() -> int:
    if len(sys.argv) != 3:
        sys.stderr.write("usage: validate-schema.py SCHEMA_FILE DOCUMENT_FILE\n")
        return 2

    try:
        import jsonschema
    except ImportError:
        sys.stderr.write(
            "validate-schema: the python 'jsonschema' package is not installed "
            "(pip install jsonschema)\n"
        )
        return 2

    schema_path, doc_path = sys.argv[1], sys.argv[2]
    try:
        with open(schema_path, encoding="utf-8") as f:
            schema = json.load(f)
        with open(doc_path, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        sys.stderr.write(f"validate-schema: {exc}\n")
        return 2

    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    for e in errors:
        path = "/".join(str(p) for p in e.absolute_path) or "(root)"
        sys.stderr.write(f"validate-schema: {doc_path}: {path}: {e.message}\n")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

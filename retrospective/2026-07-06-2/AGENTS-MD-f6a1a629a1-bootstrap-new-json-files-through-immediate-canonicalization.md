# agent instruction

**Bootstrap new JSON files through immediate canonicalization.** Creating a JSON document with the Write tool is acceptable exactly once, at birth; immediately canonicalize and lint it with scripts/jq-edit FILE '.' before doing anything else. All subsequent mutations go through jq-edit.

*Grounded in: schemas/todo.schema.json, schemas/map.json, and .claude/settings.json all bootstrapped this way this session.*

# justification

There is no jq path to create a file from nothing, so a bootstrap exception exists — but it must close instantly. The first hand-written TODO.json carried unsorted tag arrays that violated the repository's own declared convention; the linter caught it only because canonicalization ran right after creation. All three later files (the schema, the schema map, the hook settings) were written then immediately passed through `scripts/jq-edit FILE '.'`, which sorted keys, normalized indentation, and ran the linter in one step — a five-second habit. Without the habit, hand-authored files drift from canonical form at birth, the first later mutation produces a diff mixing real changes with mass reformatting, and review signal drowns in noise.

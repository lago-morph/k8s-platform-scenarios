# agent instruction

**Probe conventional subdirectories when mirroring a skill.** When copying a skill (or similar directory) from a repository whose directories you cannot list, do not rely solely on scanning SKILL.md for referenced paths — also probe the conventional subdirectories (resources/, scripts/, templates/, spec/, references/, assets/, examples/) for standard files. Reference-scanning alone misses files nothing links to.

*Grounded in: the self-retrospective skill's spec/SPEC.md missed on first copy, recovered by a later probe.*

# justification

The first import of the self-retrospective skill enumerated files by grepping SKILL.md for `resources/`, `scripts/`, and similar path references — and shipped an incomplete mirror: the skill's `spec/SPEC.md` (48 KB, the implementation-grade spec) was referenced only obliquely and the grep pattern didn't include `spec/`. The gap was found one PR later, by accident, while probing for a *different* skill's files. The fix costs one loop of HEAD-style probes against a handful of conventional names (a missing file returns a detectable sentinel); the failure costs an incomplete artifact that looks complete — the worst kind, because nothing fails until someone needs the missing file in a session that can no longer reach the source.

# Script tests

<div class="sb-card"><strong>Safety regression suite</strong><br>Tests use temporary folders and never touch real notes.</div>

## Purpose

This folder verifies path confinement, no-clobber creation, graph analysis, project-inventory exclusions, and other deterministic script behavior.

## What belongs here

- Standard-library `unittest` test modules.
- Small synthetic fixtures created at runtime in temporary directories.

## What does not belong here

- Copies of personal notes, real credentials, source documents, or project repositories.
- Network-dependent, destructive, or nondeterministic tests.

## Writers

Humans and explicitly authorized AI agents may add tests. Review test changes with the implementation they cover.

## Example

```powershell
python -m unittest discover -s tests -v
```

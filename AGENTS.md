# AGENTS.md

## Project purpose
`autograde` is a Python CLI tool that inspects a target Git repository and reports whether a set of required conditions hold.

## Dependency management
- Use `uv` for dependency management.

## Testing
- Use `pytest` for testing.
- Prefer behavioral tests over implementation-detail tests.
- Run tests with: `uv run pytest`

## Conventions
- Do not modify files in `specs/`.
- Keep the implementation as simple as possible.
- Prefer small, focused patches.
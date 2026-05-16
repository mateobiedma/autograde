# autograde

A Python CLI tool that inspects a target Git repository and reports whether a set of required conditions hold.

## Checks
- The project is a Git repository
- The `main` branch exists
- The `feature` branch exists on the remote
- `file1.txt` exists on `main`

## Requirements
- Python 3.13+
- [uv](https://github.com/astral-sh/uv)

## Installation
uv sync

## Run the tool
uv run python autograde.py <path-to-repo>

## Run the tests
uv run pytest tests/ -v
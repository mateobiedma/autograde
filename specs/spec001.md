# Spec 001: Git Repository Checker

## Behavior
- The tool accepts a path to a local directory as input.
- The tool checks whether the directory is a Git repository.
- The tool checks whether the `main` branch exists.
- The tool checks whether the `feature` branch exists on the remote.
- The tool checks whether `file1.txt` exists on the `main` branch.
- For each check, the tool reports PASSED or FAILED with a short description.

## Constraints
- The tool should be implemented in Python.
- The tool should be as simple as possible while meeting the behavior requirements.
- The tool should use `uv` for dependency management.
- The tool should use `pytest` for testing.
- The tool should be designed for maintainability and extensibility.

## Out of scope
- The tool does not need to support authentication or private repositories.
- The tool does not need to check branches other than `main` and `feature`.
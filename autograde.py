import subprocess
import sys
from pathlib import Path


def is_git_repository(path):
    """Check if the given path is a Git repository."""
    path = Path(path)
    git_dir = path / ".git"
    return git_dir.exists()


def main_branch_exists(path):
    """Check if the main branch exists in the repository."""
    path = Path(path)
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "main"],
        cwd=path,
        capture_output=True,
    )
    return result.returncode == 0


def feature_branch_on_remote(path):
    """Check if the feature branch exists on the remote."""
    path = Path(path)
    result = subprocess.run(
        ["git", "ls-remote", "origin", "feature"],
        cwd=path,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and "feature" in result.stdout


def file1_exists_on_main(path):
    """Check if file1.txt exists on the main branch."""
    path = Path(path)
    result = subprocess.run(
        ["git", "show", "main:file1.txt"],
        cwd=path,
        capture_output=True,
    )
    return result.returncode == 0


def main():
    """Run all checks on the given repository path."""
    if len(sys.argv) < 2:
        print("Usage: python autograde.py <path>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    checks = [
        ("is a Git repository", is_git_repository(path)),
        ("main branch exists", main_branch_exists(path)),
        ("feature branch exists on remote", feature_branch_on_remote(path)),
        ("file1.txt exists on main", file1_exists_on_main(path)),
    ]
    
    for description, passed in checks:
        status = "PASSED" if passed else "FAILED"
        print(f"{status}: {description}")


if __name__ == "__main__":
    main()

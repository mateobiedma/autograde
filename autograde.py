import subprocess
import sys
import tempfile
import shutil
import os
import stat
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


def _handle_remove_error(func, path, exc):
    """Handle permission errors when removing files on Windows."""
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    """Run all checks on the given repository path or GitHub URL."""
    if len(sys.argv) < 2:
        print("Usage: python autograde.py <path|github-url>")
        sys.exit(1)
    
    argument = sys.argv[1]
    temp_dir = None
    
    try:
        # Check if argument is a URL
        if argument.startswith("http://") or argument.startswith("https://"):
            # Clone to temporary directory
            temp_dir = tempfile.mkdtemp()
            result = subprocess.run(
                ["git", "clone", argument, temp_dir],
                capture_output=True,
            )
            if result.returncode != 0:
                print("FAILED: Could not clone repository")
                return
            path = temp_dir
        else:
            # Use local path
            path = argument
        
        checks = [
            ("is a Git repository", is_git_repository(path)),
            ("main branch exists", main_branch_exists(path)),
            ("feature branch exists on remote", feature_branch_on_remote(path)),
            ("file1.txt exists on main", file1_exists_on_main(path)),
        ]
        
        for description, passed in checks:
            status = "PASSED" if passed else "FAILED"
            print(f"{status}: {description}")
    finally:
        # Clean up temporary directory if created
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir, onerror=_handle_remove_error)


if __name__ == "__main__":
    main()

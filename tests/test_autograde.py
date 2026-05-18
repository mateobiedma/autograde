import subprocess
import tempfile
from pathlib import Path
import pytest

from autograde import is_git_repository, main_branch_exists, feature_branch_on_remote, file1_exists_on_main, is_valid_github_url


@pytest.fixture
def temp_repo():
    """Create a temporary Git repository with main branch and file1.txt."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        
        # Initialize repo
        subprocess.run(
            ["git", "init"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        
        # Configure git user for commits
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        
        # Create file1.txt and commit on main
        file1 = repo_path / "file1.txt"
        file1.write_text("test content")
        
        subprocess.run(
            ["git", "add", "file1.txt"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Add file1.txt"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        
        # Rename branch to main if needed
        subprocess.run(
            ["git", "branch", "-M", "main"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        
        # Create feature branch
        subprocess.run(
            ["git", "checkout", "-b", "feature"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        
        # Switch back to main
        subprocess.run(
            ["git", "checkout", "main"],
            cwd=repo_path,
            capture_output=True,
            check=True,
        )
        
        yield repo_path


@pytest.fixture
def temp_repo_with_remote(temp_repo):
    """Create a temporary bare repository and set it as remote of temp_repo."""
    with tempfile.TemporaryDirectory() as tmpdir:
        bare_repo_path = Path(tmpdir) / "bare.git"
        bare_repo_path.mkdir()
        
        # Initialize bare repository
        subprocess.run(
            ["git", "init", "--bare"],
            cwd=bare_repo_path,
            capture_output=True,
            check=True,
        )
        
        # Add remote to temp_repo
        subprocess.run(
            ["git", "remote", "add", "origin", str(bare_repo_path)],
            cwd=temp_repo,
            capture_output=True,
            check=True,
        )
        
        # Push main and feature branches to remote
        subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=temp_repo,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", "feature"],
            cwd=temp_repo,
            capture_output=True,
            check=True,
        )
        
        yield temp_repo


class TestIsGitRepository:
    """Tests for checking if directory is a Git repository."""
    
    def test_is_git_repository_valid(self, temp_repo):
        """Test that a valid Git repository is recognized."""
        assert is_git_repository(temp_repo) is True
    
    def test_is_git_repository_invalid(self):
        """Test that a non-Git directory is not recognized as a repository."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            assert is_git_repository(repo_path) is False


class TestMainBranchExists:
    """Tests for checking if main branch exists."""
    
    def test_main_branch_exists(self, temp_repo):
        """Test that main branch exists."""
        assert main_branch_exists(temp_repo) is True
    
    def test_main_branch_not_exists(self):
        """Test that main branch does not exist in non-git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            assert main_branch_exists(repo_path) is False


class TestFeatureBranchExistsOnRemote:
    """Tests for checking if feature branch exists on remote."""
    
    def test_feature_branch_on_remote(self, temp_repo_with_remote):
        """Test that feature branch exists on remote."""
        assert feature_branch_on_remote(temp_repo_with_remote) is True
    
    def test_feature_branch_not_on_remote(self, temp_repo):
        """Test that feature branch does not exist when no remote is set."""
        assert feature_branch_on_remote(temp_repo) is False


class TestFile1Exists:
    """Tests for checking if file1.txt exists on main branch."""
    
    def test_file1_exists_on_main(self, temp_repo):
        """Test that file1.txt exists on main branch."""
        assert file1_exists_on_main(temp_repo) is True
    
    def test_file1_not_exists(self):
        """Test that file1.txt does not exist in non-git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            assert file1_exists_on_main(repo_path) is False


class TestIsValidGitHubUrl:
    """Tests for validating GitHub URLs."""
    
    def test_valid_github_url(self):
        """Test that valid GitHub URLs are accepted."""
        assert is_valid_github_url("https://github.com/owner/repo") is True
    
    def test_valid_github_url_with_hyphen(self):
        """Test that GitHub URLs with hyphens in names are accepted."""
        assert is_valid_github_url("https://github.com/my-owner/my-repo") is True
    
    def test_valid_github_url_with_underscore(self):
        """Test that GitHub URLs with underscores in names are accepted."""
        assert is_valid_github_url("https://github.com/my_owner/my_repo") is True
    
    def test_valid_github_url_with_dot(self):
        """Test that GitHub URLs with dots in repo names are accepted."""
        assert is_valid_github_url("https://github.com/owner/my.repo") is True
    
    def test_invalid_github_url_http(self):
        """Test that HTTP URLs are rejected."""
        assert is_valid_github_url("http://github.com/owner/repo") is False
    
    def test_invalid_github_url_no_protocol(self):
        """Test that URLs without protocol are rejected."""
        assert is_valid_github_url("github.com/owner/repo") is False
    
    def test_invalid_github_url_wrong_domain(self):
        """Test that non-GitHub URLs are rejected."""
        assert is_valid_github_url("https://gitlab.com/owner/repo") is False
    
    def test_invalid_github_url_missing_repo(self):
        """Test that URLs without repo name are rejected."""
        assert is_valid_github_url("https://github.com/owner") is False
    
    def test_invalid_github_url_missing_owner(self):
        """Test that URLs without owner are rejected."""
        assert is_valid_github_url("https://github.com/repo") is False
    
    def test_invalid_github_url_empty_string(self):
        """Test that empty string is rejected."""
        assert is_valid_github_url("") is False
    
    def test_invalid_github_url_with_invalid_chars(self):
        """Test that URLs with invalid characters are rejected."""
        assert is_valid_github_url("https://github.com/owner@/repo") is False
        assert is_valid_github_url("https://github.com/owner/repo!") is False

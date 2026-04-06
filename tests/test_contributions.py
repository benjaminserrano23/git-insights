"""Tests for contributions analyzer."""

import os
import pytest
from git import Repo

from git_insights.analyzers.contributions import analyze_contributions


@pytest.fixture
def sample_repo(tmp_path):
    """Create a small git repo with a few commits."""
    repo = Repo.init(tmp_path)
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@test.com").release()

    # First commit
    file1 = tmp_path / "hello.py"
    file1.write_text("print('hello')\n")
    repo.index.add(["hello.py"])
    repo.index.commit("first commit")

    # Second commit
    file1.write_text("print('hello world')\nprint('goodbye')\n")
    repo.index.add(["hello.py"])
    repo.index.commit("second commit")

    # Third commit — new file
    file2 = tmp_path / "utils.py"
    file2.write_text("def add(a, b):\n    return a + b\n")
    repo.index.add(["utils.py"])
    repo.index.commit("add utils")

    return repo


def test_contributions_returns_dataframe(sample_repo):
    df = analyze_contributions(sample_repo)
    assert not df.empty
    assert "author" in df.columns
    assert "commits" in df.columns
    assert "additions" in df.columns
    assert "deletions" in df.columns


def test_contributions_commit_count(sample_repo):
    df = analyze_contributions(sample_repo)
    assert df.iloc[0]["commits"] == 3


def test_contributions_files_touched(sample_repo):
    df = analyze_contributions(sample_repo)
    assert df.iloc[0]["files_touched"] >= 2

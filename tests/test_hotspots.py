"""Tests for hotspots analyzer."""

import pytest
from git import Repo

from git_insights.analyzers.hotspots import analyze_hotspots


@pytest.fixture
def sample_repo(tmp_path):
    repo = Repo.init(tmp_path)
    repo.config_writer().set_value("user", "name", "Test User").release()
    repo.config_writer().set_value("user", "email", "test@test.com").release()

    file1 = tmp_path / "main.py"
    file2 = tmp_path / "utils.py"

    # Modify main.py 3 times, utils.py once
    file1.write_text("v1")
    repo.index.add(["main.py"])
    repo.index.commit("c1")

    file1.write_text("v2")
    repo.index.add(["main.py"])
    repo.index.commit("c2")

    file1.write_text("v3")
    file2.write_text("u1")
    repo.index.add(["main.py", "utils.py"])
    repo.index.commit("c3")

    return repo


def test_hotspots_order(sample_repo):
    df = analyze_hotspots(sample_repo)
    assert not df.empty
    # main.py should be the top hotspot
    assert df.iloc[0]["file"] == "main.py"
    assert df.iloc[0]["changes"] == 3


def test_hotspots_contains_all_files(sample_repo):
    df = analyze_hotspots(sample_repo)
    files = df["file"].tolist()
    assert "main.py" in files
    assert "utils.py" in files

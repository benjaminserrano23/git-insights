"""Integration test for core analysis."""

import pytest
from git import Repo

from git_insights.analyzers.core import run_analysis


@pytest.fixture
def sample_repo(tmp_path):
    repo = Repo.init(tmp_path)
    repo.config_writer().set_value("user", "name", "Dev").release()
    repo.config_writer().set_value("user", "email", "dev@dev.com").release()

    f = tmp_path / "app.py"
    f.write_text("print('hello')\n")
    repo.index.add(["app.py"])
    repo.index.commit("init")

    f.write_text("print('hello world')\nprint('bye')\n")
    repo.index.add(["app.py"])
    repo.index.commit("update")

    return tmp_path


def test_run_analysis(sample_repo):
    result = run_analysis(str(sample_repo))
    assert result.total_commits == 2
    assert result.total_authors == 1
    assert not result.contributions.empty
    assert not result.hotspots.empty
    assert not result.activity.empty

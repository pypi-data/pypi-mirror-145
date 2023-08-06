import os
from pathlib import Path

import pytest

from nautilus_librarian.mods.git.domain.git_user import GitUser


@pytest.fixture(scope="session")
def workflows_fixtures_dir():
    return os.path.dirname(Path(__file__).resolve())


@pytest.fixture()
def temp_git_dir(tmp_path_factory):
    fn = tmp_path_factory.mktemp("repo")
    return fn


@pytest.fixture(scope="session")
def git_user(gpg_signing_key_info):
    """
    The test committer used to create the commits in tests.
    """
    return GitUser(
        "A committer", "committer@example.com", gpg_signing_key_info["long_key"]
    )


@pytest.fixture(scope="session")
def sample_gold_image_relative_path():
    return "images/000001-32.600.2.tif"


@pytest.fixture(scope="session")
def sample_base_image_relative_path():
    return "images/000001-52.600.2.tif"


@pytest.fixture(scope="session")
def sample_gold_image_absolute_path(
    workflows_fixtures_dir, sample_gold_image_relative_path
):
    return f"{workflows_fixtures_dir}/{sample_gold_image_relative_path}"


@pytest.fixture(scope="session")
def sample_base_image_absolute_path(
    workflows_fixtures_dir, sample_base_image_relative_path
):
    return f"{workflows_fixtures_dir}/{sample_base_image_relative_path}"

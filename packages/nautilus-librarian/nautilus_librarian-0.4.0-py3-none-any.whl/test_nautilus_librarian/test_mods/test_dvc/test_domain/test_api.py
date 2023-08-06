# pylint: disable=no-member
# Dinamically added members of GIT API Repo object are not detected by pyLint

import os.path
from os import path

import pytest
from git import Repo

from nautilus_librarian.mods.dvc.domain.api import DvcApiWrapper
from nautilus_librarian.mods.dvc.domain.dvc_command_wrapper import dvc


def create_test_contents(temp_dir):
    with open(path.join(temp_dir, "test.data"), "w") as file:
        file.write("lorem ipsum")


def remove_test_contents(temp_dir):
    os.remove(f"{temp_dir}/test.data")


@pytest.fixture()
def temp_dvc_dir_with_test_content(temp_dir, temp_dvc_remote):
    DvcApiWrapper.init(temp_dir)
    dvc(temp_dir).add_local_remote_as_default("localremote", temp_dvc_remote)
    create_test_contents(temp_dir)
    return temp_dir


def push_test_contents(temp_dir):
    repo = Repo(temp_dir)
    repo.add("test.data.dvc")
    repo.push(repo.push(refspec="master:master"))


def test_api_wrapper_initialization(temp_dir):
    DvcApiWrapper.init(temp_dir)
    api = DvcApiWrapper(temp_dir)

    assert isinstance(api, DvcApiWrapper)


def test_dvc_init(temp_dir):
    DvcApiWrapper.init(temp_dir)
    DvcApiWrapper(temp_dir)

    assert path.exists(f"{temp_dir}/.dvc")


def test_diff_when_there_is_no_change(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    diff = api.diff("HEAD^", "HEAD")

    assert diff == {}


def test_add(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")

    assert path.exists(f"{temp_dvc_dir_with_test_content}/test.data.dvc")
    assert path.exists(f"{temp_dvc_dir_with_test_content}/.gitignore")


def test_move(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")
    api.move("test.data", "test_renamed.data")

    assert path.exists(f"{temp_dvc_dir_with_test_content}/test_renamed.data.dvc")
    assert not path.exists(f"{temp_dvc_dir_with_test_content}/test.data.dvc")
    assert path.exists(f"{temp_dvc_dir_with_test_content}/test_renamed.data")
    assert not path.exists(f"{temp_dvc_dir_with_test_content}/test.data")
    assert path.exists(f"{temp_dvc_dir_with_test_content}/.gitignore")


def test_remove(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")

    assert path.exists(f"{temp_dvc_dir_with_test_content}/test.data.dvc")

    api.remove("test.data.dvc")

    assert not path.exists(f"{temp_dvc_dir_with_test_content}/test.data.dvc")


def test_status(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")

    assert api.status(remote="localremote") == {"test.data": "new"}


def test_push(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")
    api.push()

    assert api.status(remote="localremote") == {}


def test_pull(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    # Add a new file
    api.add("test.data")
    assert path.exists("test.data")

    # Push the file to the remote storage
    api.push()

    # Remove the local file
    remove_test_contents(temp_dvc_dir_with_test_content)
    assert not path.exists(f"{temp_dvc_dir_with_test_content}/test.data")

    # Pull the file from remote
    api.pull()

    # The file should be pulled from remote
    assert path.exists(f"{temp_dvc_dir_with_test_content}/test.data")


def test_list(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    api.add("test.data")
    api.push()

    expected_list_output = [
        {"isout": False, "isdir": False, "isexec": False, "path": ".dvcignore"},
        {"isout": False, "isdir": False, "isexec": False, "path": ".gitignore"},
        {"isout": True, "isdir": False, "isexec": False, "path": "test.data"},
        {"isout": False, "isdir": False, "isexec": False, "path": "test.data.dvc"},
    ]
    assert api.list(temp_dvc_dir_with_test_content) == expected_list_output


def test_files_to_commit(temp_dvc_dir_with_test_content):

    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    filepaths = api.get_files_to_commit("data/000001/52/000001-52.600.2.tif")

    assert filepaths == [
        "data/000001/52/.gitignore",
        "data/000001/52/000001-52.600.2.tif.dvc",
    ]


def test_dvc_default_remote(temp_dvc_dir_with_test_content):
    api = DvcApiWrapper(temp_dvc_dir_with_test_content)

    assert api.dvc_default_remote() == "localremote"

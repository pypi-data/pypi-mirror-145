from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def test_git_test_command():
    result = runner.invoke(app, ["git", "test", "hello"])
    assert result.exit_code == 0
    assert "Testing Git module: hello" in result.stdout

from typer.testing import CliRunner

from nautilus_librarian.main import app

runner = CliRunner()


def test_gpg_test_command():
    result = runner.invoke(app, ["gpg", "test", "hello"])
    assert result.exit_code == 0
    assert "Testing GPG module: hello" in result.stdout

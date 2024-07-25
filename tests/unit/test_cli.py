import subprocess


def test_cli_0():
    result = subprocess.run(
        ["python", "cli.py", "millenium-falcon.json", "data/empire0.json"],
        capture_output=True,
    )
    assert result.returncode == 0
    print(result.stdout)
    assert result.stdout == b"Probability to succeed: 100%\n"


def test_cli_1():
    result = subprocess.run(
        ["python", "cli.py", "millenium-falcon.json", "data/empire1.json"],
        capture_output=True,
    )
    assert result.returncode == 0
    print(result.stdout)
    assert result.stdout == b"Probability to succeed: 0%\n"


def test_cli_error():
    result = subprocess.run(
        ["python", "cli.py", "jedi.json", "rebelle_alliance.json"],
        capture_output=True,
    )
    assert result.returncode == 2
    assert "Error: Invalid value for 'FALCON_FILE'" in result.stderr.decode("utf-8")

from pathlib import Path


def test_report_exists():
    """The agent produced a out file."""
    assert Path("/app/out.json").exists(), "no out.json found"


def test_report_nonempty():
    """The report file is not empty."""
    assert Path("/app/out.json").stat().st_size > 0, "out.json is empty"

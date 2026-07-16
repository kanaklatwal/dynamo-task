import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ')


def _expected():
    """Independently recompute the expected summary straight from the log."""
    paths, ips, total = Counter(), set(), 0
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        m = REQUEST_RE.search(line)
        if m:
            paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def _load_report():
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    try:
        return json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_report_exists_and_is_valid_json():
    _load_report()


def test_report_has_required_keys():
    report = _load_report()
    for key in ("total_requests", "unique_ips", "top_path"):
        assert key in report, f"report.json is missing required key '{key}'"


def test_report_field_types():
    report = _load_report()
    assert isinstance(report["total_requests"], int), "total_requests must be an integer"
    assert isinstance(report["unique_ips"], int), "unique_ips must be an integer"
    assert isinstance(report["top_path"], str), "top_path must be a string"


def test_report_values_match_log():
    report = _load_report()
    expected = _expected()
    assert report["total_requests"] == expected["total_requests"], (
        f"total_requests: expected {expected['total_requests']}, "
        f"got {report['total_requests']}"
    )
    assert report["unique_ips"] == expected["unique_ips"], (
        f"unique_ips: expected {expected['unique_ips']}, got {report['unique_ips']}"
    )
    assert report["top_path"] == expected["top_path"], (
        f"top_path: expected {expected['top_path']!r}, got {report['top_path']!r}"
    )
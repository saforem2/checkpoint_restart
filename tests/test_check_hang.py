import os
import time

from check_mate.check_hang import get_date, most_recent_mtime


def test_get_date_formats_timestamp():
    timestamp = 1_700_000_000  # fixed epoch for reproducibility
    formatted = get_date(timestamp)
    assert formatted == time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def test_most_recent_mtime_returns_latest(tmp_path):
    file_a = tmp_path / "a.out"
    file_b = tmp_path / "b.out"
    file_a.write_text("a")
    file_b.write_text("b")

    # Ensure b has a newer timestamp
    os.utime(file_b, None)

    result = most_recent_mtime([file_a, file_b])
    assert result == file_b.stat().st_mtime


def test_most_recent_mtime_ignores_missing(tmp_path):
    missing = tmp_path / "missing.dat"
    existing = tmp_path / "existing.dat"
    existing.write_text("data")

    result = most_recent_mtime([missing, existing])
    assert result == existing.stat().st_mtime


def test_most_recent_mtime_returns_none_when_empty():
    assert most_recent_mtime([]) is None

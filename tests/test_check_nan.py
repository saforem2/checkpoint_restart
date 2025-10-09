import argparse
import os
import signal
from types import SimpleNamespace

import pytest

from check_mate import check_nan


def test_split_outputs_handles_mixed_delimiters():
    specs = check_nan.split_outputs(" log1.txt:logs/*.out , result.log :: metrics.csv ")
    assert specs == ["log1.txt", "logs/*.out", "result.log", "metrics.csv"]


def test_is_glob_detects_special_characters():
    assert check_nan.is_glob("*.log")
    assert not check_nan.is_glob("logs/output.log")


def test_list_files_returns_existing_files(tmp_path):
    file_a = tmp_path / "a.log"
    file_a.write_text("hello")
    nested = tmp_path / "nested"
    nested.mkdir()
    file_b = nested / "b.log"
    file_b.write_text("world!")

    specs = [str(file_a), str(tmp_path / "*.log"), str(nested / "*.log")]
    files = check_nan.list_files(specs, recursive=False)

    assert files[str(file_a)] == len("hello")
    assert files[str(file_b)] == len("world!")


def test_scan_new_bytes_tracks_offsets(tmp_path):
    target = tmp_path / "log.txt"
    target.write_text("12345")

    end, chunk = check_nan.scan_new_bytes(str(target), 0)
    assert end == 5
    assert chunk == "12345"

    target.write_text("12345abcdef")
    end, chunk = check_nan.scan_new_bytes(str(target), end)
    assert end == len("12345abcdef")
    assert chunk == "abcdef"


def test_scan_new_bytes_missing_file_is_safe(tmp_path):
    start, chunk = check_nan.scan_new_bytes(str(tmp_path / "missing.log"), 10)
    assert start == 10
    assert chunk == ""


def test_contains_bad_tokens_detects_nan_and_inf():
    assert check_nan.contains_bad_tokens("loss=nan", include_inf=False)
    assert check_nan.contains_bad_tokens("loss=INF", include_inf=True)
    assert not check_nan.contains_bad_tokens("all good", include_inf=True)


@pytest.fixture()
def fake_sleep(monkeypatch):
    monkeypatch.setattr(check_nan.time, "sleep", lambda _: None)


def test_try_kill_pid_and_command(monkeypatch, fake_sleep, capsys):
    kills: list[tuple[int, int]] = []
    commands: list[str] = []

    def fake_kill(pid: int, sig: int) -> None:
        if sig != 0:
            kills.append((pid, sig))

    def fake_run(cmd, shell, check):
        assert shell and not check
        commands.append(cmd)

    monkeypatch.setattr(os, "kill", fake_kill)
    monkeypatch.setattr(check_nan.subprocess, "run", fake_run)

    args = argparse.Namespace(
        dry_run=False,
        pid=4242,
        signal="TERM",
        grace=1,
        kill_command="echo kill",
    )

    check_nan.try_kill(args)

    # After first invocation we expect TERM signal, escalation to SIGKILL, and the
    # kill command execution.
    assert (4242, getattr(signal, "SIGTERM")) in kills
    assert (4242, signal.SIGKILL) in kills
    assert commands == ["echo kill"]


def test_try_kill_dry_run(capsys):
    args = SimpleNamespace(
        dry_run=True,
        pid=0,
        signal="TERM",
        grace=0,
        kill_command="",
    )
    check_nan.try_kill(args)
    captured = capsys.readouterr()
    assert "[DRY-RUN] Would terminate job" in captured.out


def test_try_kill_warns_when_no_action(monkeypatch, capsys):
    args = SimpleNamespace(
        dry_run=False,
        pid=0,
        signal="TERM",
        grace=0,
        kill_command="",
    )
    check_nan.try_kill(args)
    captured = capsys.readouterr()
    assert "No kill action executed" in captured.out

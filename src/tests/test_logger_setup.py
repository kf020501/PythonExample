import logging
import sys
import json
from pathlib import Path
import pytest
from common.logger_setup import setup_logger

def teardown_function(function):
    # テスト後にロガーをリセット
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)
    root.setLevel(logging.NOTSET)


def test_console_output_levels(capsys):
    # console_enabled=True, console level=INFO
    cfg = {
        "level": "DEBUG",
        "console_output": {"enabled": True, "level": "INFO"},
        "file_output": {"enabled": False}
    }
    setup_logger(cfg)
    logger = logging.getLogger()

    # DEBUG はコンソールに出力されない
    logger.debug("debug-msg")
    # INFO はコンソールに出力される
    logger.info("info-msg")

    captured = capsys.readouterr()
    stdout = captured.out.strip().splitlines()
    assert all("debug-msg" not in line for line in stdout)
    assert any("INFO: info-msg" in line for line in stdout)


def test_file_output_and_levels(tmp_path):
    # file_enabled=True, file level=DEBUG
    log_dir = tmp_path / "logs"
    cfg = {
        "level": "INFO",
        "console_output": {"enabled": False},
        "file_output": {
            "enabled": True,
            "level": "DEBUG",
            "output_directory": str(log_dir),
            "file_prefix": "test_"
        }
    }
    setup_logger(cfg)
    logger = logging.getLogger()

    # ログ出力
    logger.debug("debug-file")
    logger.info("info-file")

    # ファイルが作成されるまで待機
    files = list(log_dir.glob("test_*.log"))
    assert files, "ログファイルが作成されていません"
    log_file = files[0]

    content = log_file.read_text(encoding="utf-8").splitlines()
    # DEBUG, INFO 両方出力される
    assert any("DEBUG: debug-file" in line for line in content)
    assert any("INFO: info-file" in line for line in content)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ロガー初期化を提供するユーティリティモジュール
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(logger_cfg):
    """
    ログ設定に基づいてloggerを初期化する。

    この関数を呼び出すと、常にコンソール出力用のハンドラを追加し、
    `enable_file_output` が True の場合はさらにファイルハンドラを追加する。
    ファイル出力時のパスは
        <log_dir>/<log_prefix><YYYYMMDD_HHMMSS>.log
    の形式となる。

    Args:
        logger_cfg (Dict[str, Any]):
            設定項目をまとめた辞書。以下のキーを解釈する：
            - level (str): ログレベル ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
            - enable_file_output (bool): ファイル出力を有効にするかどうか
            - output_directory (str): ログファイルを保存するディレクトリ
            - file_prefix (str): ログファイル名の接頭辞

    Examples:
        >>> # 初期化
        >>> logger_cfg = {
        ...     "level": "DEBUG",
        ...     "enable_file_output": true,
        ...     "output_directory": "../logs",
        ...     "file_prefix": "example_"
        ... }
        >>> setup_logger(logger_cfg)
        >>> # loggerの呼び出し(import logging と共に各関数で記載する必要がある)
        >>> logger = logging.getLogger(__name__)
    """

    # ログレベルを文字列から取得（例: "INFO" → logging.INFO）
    level_name = logger_cfg.get('level', 'INFO').upper()
    log_level = getattr(logging, level_name, logging.INFO)

    # フォーマッタを作成（YYYYMMDD hh:mm:ss.ddd）
    fmt = '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

    handlers = []

    # コンソール出力ハンドラ
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    # ファイル出力ハンドラ（log_to_file=True の場合のみ）
    if logger_cfg.get('enable_file_output', False):
        # 保存ディレクトリの準備
        base_dir = Path(__file__).resolve().parent
        log_dir = base_dir / logger_cfg.get('output_directory', 'logs')
        log_dir.mkdir(parents=True, exist_ok=True)

        # ファイル名生成：<prefix>_<YYYYMMDD_HHMMSS>.log
        prefix = logger_cfg.get('file_prefix', '')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = log_dir / f"{prefix}{timestamp}.log"

        # ファイルハンドラを作成
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # ルートロガーにまとめてハンドラを登録
    logging.basicConfig(level=log_level, handlers=handlers)

    # ロガー初期化完了メッセージ
    logging.debug("Logger initialized successfully")
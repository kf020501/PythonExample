#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サンプルスクリプト：config.json から設定を読み込み、
コンソール＋ログファイルへタイムスタンプ付きログを出力します。
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime

def load_config():
    
    """
    config.json を読み込んで dict 型で返却する関数。

    Args:
        (None)
    Returns:
        dict: config.jsonの設定内容
    """
    # スクリプト配置ディレクトリ取得
    base_dir = Path(__file__).resolve().parent
    # 設定ファイルパス
    config_path = f"{base_dir}/config.json"
    # ファイルを開いてパース
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def setup_logger(log_cfg):
    """
    log セクションの設定に従って logging を初期化する。
    log_to_fileをTrueで指定した場合、
    <log_dir>/<log_prefix>_<YYYYMMDD_HHMMSS>.log に出力される。

    Args:
        dict: ログの設定
            log_level: ログ出力レベル(初期値: INFO)
            log_to_file: ファイルに出力するか(初期値: False)
            log_dir: 出力先ディレクトリ(初期値: log)
            log_prefix: ログファイル名の接頭語(初期値: python)
    Returns:
        (None)
    """

    # ログレベルを文字列から取得（例: "INFO" → logging.INFO）
    level_name = log_cfg.get('log_level', 'INFO').upper()
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
    if log_cfg.get('log_to_file', False):
        # 保存ディレクトリの準備
        base_dir = Path(__file__).resolve().parent
        log_dir = base_dir / log_cfg.get('log_dir', 'logs')
        log_dir.mkdir(parents=True, exist_ok=True)

        # ファイル名生成：<prefix>_<YYYYMMDD_HHMMSS>.log
        prefix = log_cfg.get('log_prefix', 'app')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = log_dir / f"{prefix}_{timestamp}.log"

        # ファイルハンドラを作成
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # ルートロガーにまとめてハンドラを登録
    logging.basicConfig(level=log_level, handlers=handlers)


def get_input_interactive():
    """
    対話式で変数を取得する関数のサンプル
    """
    default_name = 'none_name'
    your_name = input(f'あなたの名前を入力してください [{default_name}]: ') or default_name
    return your_name

def main(args):

    # --------------------------------------------------------------------------
    # 初期化
    # --------------------------------------------------------------------------

    # 設定読み込み
    config = load_config()
    # configのlog セクションを切り抜いてロガーに渡す
    log_cfg = config.get('log', {})
    setup_logger(log_cfg)
    # 名前付きロガー取得
    logger = logging.getLogger(__name__)

    # --------------------------------------------------------------------------
    # 変数定義
    # --------------------------------------------------------------------------

    len_args = len(args)
    logger.debug(f'引数の個数は{str(len_args)}です')

    # コマンド引数が不足していたら対話式で取得
    if len(args) == 2:
        logger.debug('引数がありました。')
        your_name = args[1]
    else:
        logger.debug('引数が不足していたため、対話式処理を開始します。')
        your_name = get_input_interactive()

    # --------------------------------------------------------------------------
    # メイン処理
    # --------------------------------------------------------------------------

    logger.debug('処理を開始します')
    logger.info(f'あなたの名前は{your_name}です')

    logger.debug('処理が完了しました')

    return your_name

if __name__ == '__main__':
    # スクリプトが直接実行された場合に main() を呼び出す
    main(sys.argv)

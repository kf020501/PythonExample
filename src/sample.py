#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サンプルスクリプト：config.json から設定を読み込み、
コンソール＋ログファイルへタイムスタンプ付きログを出力します。
"""
import logging
import sys
import uuid6
from common.config_loader import load_config
from common.logger_setup import setup_logger


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
    config = load_config('config.json', base_path=__file__)

    # configのlogger セクションを切り抜いてロガーを初期化
    logger_cfg = config.get('logger', {})
    setup_logger(logger_cfg)
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

    # UUIDv7を取得
    u7 = uuid6.uuid7()

    logger.info(f'あなたのUUIDは{u7}です')
    logger.info(f'あなたの名前は{your_name}です')

    logger.debug('処理が完了しました')

    return your_name

if __name__ == '__main__':
    # スクリプトが直接実行された場合に main() を呼び出す
    main(sys.argv)

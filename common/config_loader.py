#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ファイル(config.json)の読み込みを提供するユーティリティモジュール
"""
import json
from pathlib import Path

def load_config(config_file, base_path = None):
    """
    指定されたパスの JSON 設定ファイルを読み込んで dict を返却。

    Args:
        config_file (Union[str, Path]):
            設定ファイルへのパス。絶対パスまたは相対パスを指定可能。
        base_path (Optional[Union[str, Path]]):
            相対パス解決の基準パス。
            - スクリプト(__file__)のパスを指定すると、そのスクリプトと同階層を基準にできる。
            - 指定しない場合は CWD を使用。

    Returns:
        dict: パースされた設定データ

    Examples:
        # 呼び出し元スクリプトの存在するディレクトリを基準に読み込む
        >>> cfg = load_config('config.json', base_path=__file__)

        # カレントディレクトリ基準で読み込む
        >>> cfg = load_config('config/default.json')
    """
    # Path オブジェクト化
    path = Path(config_file)

    # 絶対パスかを判定
    if not path.is_absolute():
        # 相対パスの場合
        if base_path:
            # base_path が指定されていればその位置を起点に
            base = Path(base_path)
            # base_path にファイルが渡された場合は親ディレクトリを使用
            if base.is_file():
                base = base.parent
            # base を起点に相対パスを結合
            path = base / path
        else:
            # base_path 未指定 → 現在の作業ディレクトリ(CWD)を起点に
            path = Path.cwd() / path

    # 存在チェック
    if not path.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")
    
    # JSON パース
    with path.open('r', encoding='utf-8') as f:
        config = json.load(f)

    # 読み込んだ設定を返却
    return config

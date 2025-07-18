PythonExample
================================================================================

Pythonのサンプルリポジトリ(テンプレートとして使いまわす用)  

- ログの出力(コンソールおよびログファイル)
- jsonの記載内容取得
- 対話式での変数取得
- pytestによるテスト自動化
- DockerfileおよびMakefile


使用方法
--------------------------------------------------------------------------------

### 前提条件

Dockerがインストールされていること

### 初回セットアップ

1. リポジトリをクローンまたはファイルを配置
2. コンテナをビルド

```bash
git clone <リポジトリURL>
cd <ディレクトリ>
make build
```

### 実行

```bash
# コンテナに入る
make run

# srcディレクトリに移動し、sample.pyを実行
python sample.py your_name
```

### テストの実行

```sh
# テストの実行
pytest

# 詳細ログを出力したい場合
pytest --log-cli-level=DEBUG
```


設計
--------------------------------------------------------------------------------

### リポジトリ構成

```
.
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
└── src                 # ここより下がコンテナにマウントされる
    ├── config.json     # 設定ファイル
    ├── sample.py       # メインのサンプルファイル
    ├── common          # 共通モジュールを格納
    │   ├── __init__.py
    │   ├── config_loader.py
    │   └── logger_setup.py
    └── tests           # テストコードの格納
        ├── __init__.py
        ├── test_logger_setup.py
        └── test_main.py
```

### config.jsonの内容

logセクションで、setup_logger関数の設定が可能

```json
{
    "logger": {
        "level": "INFO",        // ルートロガーのレベル (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        "console_output": {     // ログのコンソール出力の設定
            "enabled": true,
            "level": "INFO"
        },
        "file_output": {        // ログのファイル出力の設定
            "enabled": true,
            "level": "DEBUG",
            "output_directory": "../logs",
            "file_prefix": "example_"
        }
    }
}
```


Note
--------------------------------------------------------------------------------

### commit メッセージの書き方

1行目は`<Type>: <Title>`の形式で記載し、3行目以降に詳細を記載する。  
例:
```
update: ユーザー認証の新機能を追加

- ログイン機能を実装
- パスワード暗号化を追加
- 認証モジュールの単体テストを作成
```

| Type         | 説明                                                             |
| ------------ | ---------------------------------------------------------------- |
| First Commit | 初回コミット                                                     |
| Update       | 機能の追加や更新                                                 |
| Fix          | バグ修正                                                         |
| Refactor     | コードのリファクタリング                                         |
| Chore        | 機能には影響しない更新のみ<br>ドキュメント、テスト機能の変更など |


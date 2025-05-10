from src import sample

def test_main():

    your_name = "test_name"

    # スクリプト引数を受け取る仕様のため、第一引数はダミー
    result = sample.main(["dummy_path", your_name])
    assert result == your_name

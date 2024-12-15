

# 初期表示のテスト
def test_index(create_client):
    # views.pyのindexメソッドを呼び出し
    result = create_client.get('/')

    # HTTPステータスコードと遷移先画面のタイトルを確認
    assert 200 == result.status_code
    assert "<title>入力画面</title>" in result.data.decode('utf-8')

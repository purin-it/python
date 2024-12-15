import pytest


# 入力項目の設定(正常)
@pytest.fixture
def create_post_data_normal():
    post_data = dict()
    post_data["name"] = "テスト　プリン１"
    post_data["birthYear"] = "2005"
    post_data["birthMonth"] = "9"
    post_data["birthDay"] = "21"
    post_data["sex"] = "2"
    post_data["memo"] = "これはテストです。"
    post_data["checked"] = "on"
    return post_data


# 入力項目の設定(全項目なし)
@pytest.fixture
def create_post_data_none():
    post_data = dict()
    post_data["name"] = ""
    post_data["birthYear"] = ""
    post_data["birthMonth"] = ""
    post_data["birthDay"] = ""
    post_data["sex"] = ""
    post_data["memo"] = ""
    post_data["checked"] = ""
    return post_data


# 入力項目の設定(全項目あり_生年月日エラー)
@pytest.fixture
def create_post_data_err_birthday():
    post_data = dict()
    post_data["name"] = "テスト　プリン１"
    post_data["birthYear"] = "2012"
    post_data["birthMonth"] = "2"
    post_data["birthDay"] = "31"
    post_data["sex"] = "2"
    post_data["memo"] = "これはテストです。"
    post_data["checked"] = "on"
    return post_data


# 正常時のテスト
def test_confirm_normal(create_client, create_post_data_normal):
    # views.pyのconfirmメソッドを呼び出し
    result = create_client.post("/confirm", data=create_post_data_normal)

    # HTTPステータスコードと遷移先画面のタイトルを確認
    assert 200 == result.status_code
    assert "<title>確認画面</title>" in result.data.decode('utf-8')

    # 遷移先画面に入力項目の各値が設定されていることを確認
    assert "テスト　プリン１" in result.data.decode('utf-8')
    assert "2005年9月21日" in result.data.decode('utf-8')
    assert "女" in result.data.decode('utf-8')
    assert "これはテストです。" in result.data.decode('utf-8')
    assert "確認済" in result.data.decode('utf-8')


# 必須入力エラー時のテスト
def test_confirm_error_none(create_client, create_post_data_none):
    # views.pyのconfirmメソッドを呼び出し
    result = create_client.post("/confirm", data=create_post_data_none)

    # HTTPステータスコードと遷移先画面のタイトルを確認
    assert 200 == result.status_code
    assert "<title>入力画面</title>" in result.data.decode('utf-8')

    # それぞれのエラーメッセージが表示されていることを確認
    assert "名前を入力してください。" in result.data.decode('utf-8')
    assert "生年月日を入力してください。" in result.data.decode('utf-8')
    assert "性別を指定してください。" in result.data.decode('utf-8')
    assert "入力確認をチェックしてください。" in result.data.decode('utf-8')


# 生年月日存在チェックエラー時のテスト
def test_confirm_normal(create_client, create_post_data_err_birthday):
    # views.pyのconfirmメソッドを呼び出し
    result = create_client.post("/confirm", data=create_post_data_err_birthday)

    # HTTPステータスコードと遷移先画面のタイトルを確認
    assert 200 == result.status_code
    assert "<title>入力画面</title>" in result.data.decode('utf-8')

    # 生年月日存在チェックエラーのメッセージが表示されていることを確認
    assert "生年月日が存在しない日付になっています。" in result.data.decode('utf-8')

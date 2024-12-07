import pytest
from demo import app


# 各テストコードで共通する処理
@pytest.fixture
def create_client():
    app.config['TESTING'] = True
    return app.test_client()

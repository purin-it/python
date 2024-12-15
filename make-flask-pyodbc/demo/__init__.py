from flask import Flask

# Flaskオブジェクトを作成する
app = Flask(__name__)

# Flashメッセージを利用するための設定
app.secret_key = 'flash_key'

# demoフォルダ内のviews.pyを実行する
import demo.views

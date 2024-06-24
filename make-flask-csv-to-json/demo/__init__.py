from flask import Flask

# Flaskオブジェクトを作成する
app = Flask(__name__)

# demoフォルダ内のviews.pyを実行する
import demo.views

from demo import app
from flask import render_template, request


# 初期表示処理
@app.route("/")
def index():
    return render_template("input.html")


# 確認画面遷移処理
@app.route("/confirm", methods=["POST"])
def confirm():
    return render_template("confirm.html", form_data=request.form)


# 確認画面_完了画面遷移処理
@app.route("/send", methods=["POST"])
def send():
    return render_template("complete.html")


# 確認画面_戻るボタン押下処理
@app.route("/back", methods=["POST"])
def back():
    return render_template("input.html", form_data=request.form)

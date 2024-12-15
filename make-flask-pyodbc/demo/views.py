from demo import app
from flask import render_template, request
from .checks import CheckInputForm
from .regist import RegistInputForm


# 初期表示処理
@app.route("/")
def index():
    return render_template("input.html")


# 入力画面_確認ボタン押下処理
@app.route("/confirm", methods=["POST"])
def confirm():
    # 入力画面の項目チェックでエラーになった場合は、入力画面に遷移する
    chk_rslt = CheckInputForm(request.form).check()
    if not chk_rslt:
        return render_template("input.html", form_data=request.form)
    # 入力画面の項目チェックで正常な場合は、確認画面に遷移する
    return render_template("confirm.html", form_data=request.form)


# 確認画面_送信ボタン押下処理
@app.route("/send", methods=["POST"])
def send():
    # 登録処理を呼び出し、エラーが有る場合は、画面遷移しない
    has_error = RegistInputForm(request.form).regist()
    if has_error:
        return render_template("confirm.html", form_data=request.form)
    # 登録処理を呼び出し、エラーが無い場合は、完了画面に遷移する
    return render_template("complete.html")


# 確認画面_戻るボタン押下処理
@app.route("/back", methods=["POST"])
def back():
    return render_template("input.html", form_data=request.form)

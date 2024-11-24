from flask import flash
from datetime import datetime


# 入力画面の項目チェックを行う
class CheckInputForm:

    # 初期化処理
    def __init__(self, form):
        self.form = form

    # 項目チェック処理
    def check(self):
        # チェックエラーの有無を設定する
        chk_rslt = True
        # 各項目値を取得
        name = self.form.get('name')
        birth_year = self.form.get('birthYear')
        birth_month = self.form.get('birthMonth')
        birth_day = self.form.get('birthDay')
        sex = self.form.get('sex')
        checked = self.form.get('checked')
        # 各項目の入力チェック
        # 名前
        if not name:
            flash('名前を入力してください。')
            chk_rslt = False
        # 生年月日
        if not birth_year and not birth_month and not birth_day:
            flash('生年月日を入力してください。')
            chk_rslt = False
        else:
            birth_day_ymd = birth_year.zfill(4) + birth_month.zfill(2) + birth_day.zfill(2)
            try:
                datetime.strptime(birth_day_ymd, "%Y%m%d")
            except ValueError:
                flash('生年月日が存在しない日付になっています。')
                chk_rslt = False
        # 性別
        if not sex:
            flash('性別を指定してください。')
            chk_rslt = False
        # 入力確認
        if not checked:
            flash('入力確認をチェックしてください。')
            chk_rslt = False
        return chk_rslt

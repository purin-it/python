from flask import flash
import pyodbc


class RegistInputForm:
    # SQL Server接続情報
    DRIVER_NAME = '{ODBC Driver 17 for SQL Server}'
    SERVER_NAME = 'localhost'
    DATABASE_NAME = 'master'
    USER_ID = 'USER01'
    PASSWORD = 'USER01'

    # 初期化処理
    def __init__(self, form):
        self.form = form

    # 登録処理
    def regist(self):
        # エラーの有無を設定する
        has_error = False
        # 各項目値を取得
        name = self.form.get('name')
        birth_year = self.form.get('birthYear')
        birth_month = self.form.get('birthMonth')
        birth_day = self.form.get('birthDay')
        sex = self.form.get('sex')
        memo = self.form.get('memo')
        # SQL Serverに接続
        conn = pyodbc.connect('DRIVER=' + self.DRIVER_NAME + ';SERVER=' + self.SERVER_NAME
                              + ';DATABASE=' + self.DATABASE_NAME + ';UID=' + self.USER_ID
                              + ';PWD=' + self.PASSWORD)
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            # 登録済のid最大値を取得し設定
            max_id = 0
            cursor.execute('SELECT IsNull(MAX(id), 0) FROM dbo.USER_DATA')
            for row in cursor:
                max_id = row[0]
            # 登録処理
            cursor.execute("INSERT INTO dbo.USER_DATA ("
                           + " id, name, birth_year, birth_month, birth_day, sex, memo "
                           + ") VALUES (" + str(int(max_id) + 1) + ",N'" + name + "'," + birth_year
                           + "," + birth_month + "," + birth_day + ",'" + sex + "',N'" + memo + "')")
            conn.commit()
        except pyodbc.Error as ex:
            print(ex)
            flash('予期せぬエラーが発生しました、管理者に連絡してください。')
            has_error = True
            conn.rollback()
        # データベース接続を終了する
        cursor.close()
        conn.close()
        return has_error

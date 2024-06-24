from demo import app
from flask import render_template, request
from .csv_json import CsvToJson


# 初期表示処理
@app.route("/")
def index():
    return render_template("index.html", json_txt="")


# CSV取込ボタン押下処理
@app.route('/import-csv', methods=['POST'])
def import_csv():
    # アップロードしたCSVファイルを保存し、CSVファイルのデータをJSONに変換する
    csv_json = CsvToJson(request.files.get("csv_file"))
    json_txt = csv_json.upload_csv_to_json()

    # JSONに変換したCSVデータを設定し、画面遷移する
    return render_template("index.html", json_txt=json_txt)

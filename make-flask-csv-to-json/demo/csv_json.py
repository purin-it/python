import json
import csv
from chardet import detect


# CSVファイルのデータをチェックし、JSONに変換するクラス
class CsvToJson:

    # 引数にCSVファイルを渡してインスタンスを生成
    def __init__(self, req_file):
        self.req_file = req_file

    # アップロードしたCSVファイルを保存し、
    # CSVファイルのデータをJSONに変換して返す
    def upload_csv_to_json(self):
        # アップロードしたCSVファイルを保存
        req_file_path = "./demo/upload/" + self.req_file.filename
        self.req_file.save(req_file_path)

        # CSVファイルの文字コードを判定
        # 判定した文字コードがSHIFT_JISの場合は、CP932に変換する
        f = open(req_file_path, 'rb')
        rawdata = f.read()
        f.close()
        encoding = detect(rawdata)['encoding']
        if "SHIFT_JIS" == encoding:
            encoding = "CP932"

        # アップロードしたCSVファイルを読み込み、json_listに追加する
        json_list = []
        f = open(req_file_path, 'r', encoding=encoding)
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            json_list.append(row)
        f.close()

        # json_listをJSON形式に変換した値を返す
        # ensure_ascii=Falseを指定することで、日本語のままJSON文字列を出力する
        # indent=2を指定することで、読みやすく改行したJSON文字列になる
        return json.dumps(json_list, ensure_ascii=False, indent=2)

from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm
from .models import UserData
from django.db.models import Max
from datetime import datetime as dt

# クラス定数を定義
SEX_LABEL_IDX = 1  # 性別のラベルを取得するためのインデックス


def index(request):
    """ 入力画面を表示 """
    # 確認画面に渡すフォームを初期化
    params = {
        'input_form': InputForm()
    }
    return render(request, 'demo/input.html', params)


def confirm(request):
    """ 入力画面で確認ボタンが押下された時の処理を定義 """
    # 入力画面でのフォーム値を取得し
    input_form = InputForm(request.POST)

    # フォームの入力チェックを行い、エラーがない場合
    if input_form.is_valid():
        # 確認画面で表示するための入力値(生年月日・性別)の値を生成
        lbl_birth_day = request.POST['birth_day_year'] + '年' \
                        + request.POST['birth_day_month'] + '月' \
                        + request.POST['birth_day_day'] + '日'
        lbl_sex = input_form.sex_data[int(request.POST['sex']) - 1][SEX_LABEL_IDX]

        # 確認画面に渡す各変数を定義
        params = {
            'input_form': input_form,
            'lbl_birth_day': lbl_birth_day,
            'lbl_sex': lbl_sex,
            'lbl_checked': '確認済'
        }
        return render(request, 'demo/confirm.html', params)

    # フォームの入力チェックを行い、エラーがある場合
    else:
        # フォーム値はそのままで入力画面に戻る
        params = {
            'input_form': input_form
        }
        return render(request, 'demo/input.html', params)


def regist(request):
    """ 確認画面でボタンが押下された時の処理を定義 """
    # 送信ボタンが押下された場合
    if "send" in request.POST:
        # USER_DATAテーブルに登録されているidの最大値を取得
        max_id_dict = UserData.objects.all().aggregate(Max('id'))

        # USER_DATAテーブルに入力データを追加
        # USER_DATAテーブルに登録されているデータが無い場合、id=1とする
        id = (max_id_dict['id__max'] or 0) + 1
        name = request.POST['name']
        birth_day_dt = dt.strptime(request.POST['birth_day'], '%Y-%m-%d')
        birth_year = birth_day_dt.year
        birth_month = birth_day_dt.month
        birth_day = birth_day_dt.day
        sex = request.POST['sex']
        # メモは未設定の場合はNULLを設定するようにする
        memo = None if len(request.POST['memo']) == 0 else request.POST['memo']
        user_data = UserData(id=id, name=name, sex=sex, birth_year=birth_year,
                             birth_month=birth_month, birth_day=birth_day, memo=memo)
        user_data.save()
        return render(request, 'demo/complete.html')

    # 戻るボタンが押下された場合
    elif "back" in request.POST:
        # 確認画面でのフォーム値を入力画面に渡す
        input_form = InputForm(request.POST)
        params = {
            'input_form': input_form
        }
        return render(request, 'demo/input.html', params)

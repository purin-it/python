from django.shortcuts import render
from django.http import HttpResponse
from .forms import InputForm

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
        # 将来的に、ここにDB登録処理を実装する予定
        return render(request, 'demo/complete.html')

    # 戻るボタンが押下された場合
    elif "back" in request.POST:
        # 確認画面でのフォーム値を入力画面に渡す
        input_form = InputForm(request.POST)
        params = {
            'input_form': input_form
        }
        return render(request, 'demo/input.html', params)

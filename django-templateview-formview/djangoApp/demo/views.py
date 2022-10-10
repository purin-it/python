from django.shortcuts import render
from .forms import InputModelForm
from .models import UserData
from django.db.models import Max
from datetime import datetime as dt
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy

# クラス定数を定義
SEX_LABEL_IDX = 1  # 性別のラベルを取得するためのインデックス


class IndexView(TemplateView):
    """ 入力画面を表示するView """
    template_name = 'demo/input.html'

    def get_context_data(self):
        """ 入力画面に渡すフォーム値を初期化 """
        context = super().get_context_data()
        context['input_form'] = InputModelForm()
        return context


class ConfirmView(FormView):
    """ 入力画面で確認ボタンが押下された時の処理を定義するView """
    template_name = 'demo/input.html'   # form_invalidメソッド実行時に表示する画面
    form_class = InputModelForm         # 利用するFormクラス
    success_url = 'demo/confirm.html'   # form_validメソッド実行時の画面遷移先

    def get_context_data(self, form):
        """ 入力チェックエラー時に、入力画面にフォーム値を渡す """
        context = super().get_context_data()
        context['input_form'] = form
        return context

    def form_valid(self, form):
        """ フォームの入力チェックを行い、エラーがない場合 """
        # 確認画面で表示するための入力値(性別)の値を生成
        lbl_sex = UserData.sex_data[int(form.cleaned_data['sex']) - 1][SEX_LABEL_IDX]

        # 確認画面に渡す各変数を定義し、確認画面に遷移
        context = {
            'input_form': form,
            'lbl_sex': lbl_sex,
            'lbl_checked': '確認済'
        }
        return render(self.request, self.success_url, context)

    def form_invalid(self, form):
        """ フォームの入力チェックを行い、エラーがある場合 """
        # フォーム値はそのままで入力画面に戻る
        return super().form_invalid(form)


class RegistView(FormView):
    """ 確認画面でボタンが押下された時の処理を定義するView """
    template_name = 'demo/input.html'        # 戻るボタン押下時に表示する画面
    form_class = InputModelForm              # 利用するFormクラス
    success_url = reverse_lazy('complete')   # 送信ボタン押下後の画面遷移先

    def get_context_data(self, form):
        """ 戻るボタン押下時に、入力画面にフォーム値を渡す """
        context = super().get_context_data()
        context['input_form'] = form
        return context

    def form_valid(self, form):
        # 送信ボタンが押下された場合
        if "send" in self.request.POST:
            # USER_DATAテーブルに登録されているidの最大値を取得
            max_id_dict = UserData.objects.all().aggregate(Max('id'))

            # USER_DATAテーブルに入力データを追加
            # USER_DATAテーブルに登録されているデータが無い場合、id=1とする
            user_data = UserData()
            user_data.id = (max_id_dict['id__max'] or 0) + 1

            # 確認画面でのフォーム値にidを設定し、入力データを保存
            input_form = InputModelForm(self.request.POST, instance=user_data)
            input_form.save()

            # 完了画面に遷移
            return super().form_valid(form)

        # 戻るボタンが押下された場合
        elif "back" in self.request.POST:
            # 確認画面でのフォーム値を入力画面に渡す
            return super().form_invalid(form)


class CompleteView(TemplateView):
    """ 完了画面を表示するView """
    template_name = 'demo/complete.html'

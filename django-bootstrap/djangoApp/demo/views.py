from django.shortcuts import render
from .forms import InputModelForm
from .models import UserData
from django.db.models import Max
from datetime import datetime as dt
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

# クラス定数を定義
SEX_LABEL_IDX = 1  # 性別のラベルを取得するためのインデックス


class UserListView(ListView):
    """ 一覧画面を表示するView """
    template_name = 'demo/list.html'  # 一覧画面のHTML
    model = UserData  # UserDataモデル(user_dataテーブルと紐づける)
    context_object_name = 'user_list'  # 一覧取得結果


class InputView(TemplateView):
    """ 入力画面を表示するView """
    template_name = 'demo/input.html'

    def get_context_data(self):
        """ 入力画面に渡すフォーム値を初期化 """
        context = super().get_context_data()
        context['form'] = InputModelForm()
        return context

    def post(self, request):
        """ 入力画面にpostリクエストで遷移 """
        return render(request, self.template_name, self.get_context_data())


class ConfirmView(FormView):
    """ 入力画面で確認ボタンが押下された時の処理を定義するView """
    template_name = 'demo/input.html'  # form_invalidメソッド実行時に表示する画面
    form_class = InputModelForm  # 利用するFormクラス
    success_url = 'demo/confirm.html'  # form_validメソッド実行時の画面遷移先

    def get_context_data(self, form):
        """ 入力チェックエラー時に、入力画面にuser_idの値を渡す """
        context = super().get_context_data()
        context['user_id'] = self.request.POST['user_id']
        return context

    def form_valid(self, form):
        """ フォームの入力チェックを行い、エラーがない場合 """
        # 確認画面で表示するための入力値(性別)の値を生成
        lbl_sex = UserData.sex_data[int(form.cleaned_data['sex']) - 1][SEX_LABEL_IDX]

        # 確認画面に渡す各変数を定義し、確認画面に遷移
        context = {
            'input_form': form,
            'lbl_sex': lbl_sex,
            'lbl_checked': '確認済',
            'user_id': self.request.POST['user_id']
        }
        return render(self.request, self.success_url, context)

    def form_invalid(self, form):
        """ フォームの入力チェックを行い、エラーがある場合 """
        # フォーム値はそのままで入力画面に戻る
        return super().form_invalid(form)


class RegistView(FormView):
    """ 確認画面でボタンが押下された時の処理を定義するView """
    template_name = 'demo/input.html'  # 戻るボタン押下時に表示する画面
    form_class = InputModelForm  # 利用するFormクラス
    success_url = reverse_lazy('complete')  # 送信ボタン押下後の画面遷移先

    def get_context_data(self, form):
        """ 戻るボタン押下時に、入力画面にフォーム値を渡す """
        context = super().get_context_data()
        context['input_form'] = form
        context['user_id'] = self.request.POST['user_id']
        return context

    def form_valid(self, form):
        # 送信ボタンが押下された場合
        if "send" in self.request.POST:
            # 入力データを生成
            user_data = UserData()
            # user_idの値をリクエストから取得
            user_id = self.request.POST['user_id']

            # user_idが設定済(更新)の場合
            if user_id:
                user_data.id = int(user_id)
            # user_idが未設定(追加)の場合
            else:
                # USER_DATAテーブルに登録されているidの最大値を取得
                max_id_dict = UserData.objects.all().aggregate(Max('id'))
                # USER_DATAテーブルに登録されているデータが無い場合、id=1とする
                user_data.id = (max_id_dict['id__max'] or 0) + 1

            # 入力データを保存
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


class UserDeleteView(DeleteView):
    """ 一覧画面で削除リンクが押下された時の処理を定義するView """
    template_name = 'demo/delete_confirm.html'  # 削除確認画面を表示
    model = UserData  # UserDataモデル(user_dataテーブルと紐づける)
    success_url = reverse_lazy('index')  # 削除ボタン押下後の画面遷移先


class UserUpdateView(UpdateView):
    """ データ更新時の入力画面を表示するView """
    template_name = 'demo/input.html'
    model = UserData  # UserDataモデル(user_dataテーブルと紐づける)
    form_class = InputModelForm  # 利用するFormクラス

from django import forms
from .models import UserData
from django.core.validators import RegexValidator
import datetime


def check_date(year, month, day):
    """ 年月日が存在する日付の場合はTrue、存在しない日付の場合はFalseを返す """
    try:
        new_date_str = "%04d/%02d/%02d" % (year, month, day)
        datetime.datetime.strptime(new_date_str, "%Y/%m/%d")
        return True
    except ValueError:
        return False


class UserDataModelForm(forms.ModelForm):
    """ user_dataテーブルへアクセスするためのモデルに準じたフォーム """
    class Meta:
        # ベースとなるモデルクラス(UserData)を指定
        model = UserData
        # ベースとなるモデルクラスのうち、表示するフィールドを指定
        fields = ('name', 'birth_year', 'birth_month', 'birth_day', 'sex', 'memo')
        labels = {
            'name': '名前',
            'birth_day': '生年月日',
            'sex': '性別',
            'memo': 'メモ',
        }
        widgets = {
            'name': forms.TextInput(attrs={'size': '13', 'maxlength': '13'}),
            'birth_year': forms.Select,
            'birth_month': forms.Select,
            'birth_day': forms.Select,
            'sex': forms.RadioSelect(),
            'memo': forms.Textarea(attrs={'rows': 6, 'cols': 40}),
        }

    def clean(self):
        """ フォーム内の項目の入力チェック処理 """
        cleaned_data = super().clean()
        birth_year = cleaned_data.get('birth_year')
        birth_month = cleaned_data.get('birth_month')
        birth_day = cleaned_data.get('birth_day')

        # 生年月日が存在しない日付の場合、エラーを返す
        if not check_date(birth_year, birth_month, birth_day):
            raise forms.ValidationError('生年月日を正しく入力してください。')
        return cleaned_data


class InputModelForm(UserDataModelForm):
    """ user_dataテーブルへアクセスするためのモデルに準じたフォームに、項目(check)を追加 """
    """ views.pyからは、このInputModelFormクラスを参照している """
    check = forms.BooleanField(label='入力確認')

    class Meta(UserDataModelForm.Meta):
        fields = UserDataModelForm.Meta.fields + ('check',)
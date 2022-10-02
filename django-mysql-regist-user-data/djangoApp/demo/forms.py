from django import forms


class InputForm(forms.Form):
    sex_data = [
        ('1', '男'),
        ('2', '女')
    ]
    name = forms.CharField(label='名前', max_length=13)
    birth_day = forms.DateField(label='生年月日'
                                , widget=forms.SelectDateWidget(years=range(1910, 2023))
                                , initial='2012-01-01')
    sex = forms.ChoiceField(label='性別', choices=sex_data
                            , widget=forms.RadioSelect())
    memo = forms.CharField(label='メモ'
                           , widget=forms.Textarea(attrs={'rows': 6, 'cols': 40})
                           , required=False)
    check = forms.BooleanField(label='入力確認')

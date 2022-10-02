from django.db import models


class UserData(models.Model):
    """ user_dataテーブルへアクセするためのモデル """

    # テーブル名を存在するuser_dataテーブルに変更する
    class Meta:
        db_table = 'user_data'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)
    birth_year = models.IntegerField()
    birth_month = models.IntegerField()
    birth_day = models.IntegerField()
    sex = models.CharField(max_length=1)
    memo = models.CharField(max_length=1024, null=True)

    # print(UserDataオブジェクト)とすることで、UserDataオブジェクトの各値を
    # 文字列で表示できるようにするためのメソッド
    def __str__(self):
        return 'UserData id=' + str(self.id) + ', name=' + str(self.name) \
               + ', birth_year=' + str(self.birth_year) \
               + ', birth_month=' + str(self.birth_month) \
               + ', birth_day=' + str(self.birth_day) \
               + ', sex=' + str(self.sex) + ', memo=' + str(self.memo)

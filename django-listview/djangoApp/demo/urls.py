from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='index'),
    path('input', views.InputView.as_view(), name='input'),
    path('confirm', views.ConfirmView.as_view(), name='confirm'),
    path('regist', views.RegistView.as_view(), name='regist'),
    path('complete', views.CompleteView.as_view(), name='complete'),
]

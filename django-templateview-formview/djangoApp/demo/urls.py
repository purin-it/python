from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('confirm', views.ConfirmView.as_view(), name='confirm'),
    path('regist', views.RegistView.as_view(), name='regist'),
    path('complete', views.CompleteView.as_view(), name='complete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list', views.UserListView.as_view(), name='list'),
    path('move_page/<int:next_page>', views.MovePageView.as_view(), name='move_page'),
    path('search', views.SearchView.as_view(), name='search'),
    path('input', views.InputView.as_view(), name='input'),
    path('confirm', views.ConfirmView.as_view(), name='confirm'),
    path('regist', views.RegistView.as_view(), name='regist'),
    path('complete', views.CompleteView.as_view(), name='complete'),
    path('<int:pk>/update', views.UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.UserDeleteView.as_view(), name='delete'),
]

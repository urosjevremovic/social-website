from django.urls import path
from django.contrib.auth.views import (logout, LoginView, logout_then_login, )

from account.views import RegisterView, Edit, edit
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<code>/', views.activate_user_view, name='activate'),
    path('edit/', Edit.as_view(), name='edit'),
    path('logout_then_login/', logout_then_login, name='logout_then_login'),
    path('', views.dashboard, name='dashboard'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]

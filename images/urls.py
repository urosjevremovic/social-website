from django.urls import path
from . import views


app_name = 'images'
urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('ranking/', views.image_ranking, name='ranking'),
    path('', views.image_list, name='list'),
    path('users_images/', views.users_image_list, name='users_image_list')
]
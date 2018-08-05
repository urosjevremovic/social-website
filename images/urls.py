from django.urls import path

from images.views import ImageCreate, ImageDetail, ImageRanking, ImageDelete
from . import views


app_name = 'images'
urlpatterns = [
    path('create/', ImageCreate.as_view(), name='create'),
    path('detail/<int:id>/<slug:slug>/', ImageDetail.as_view(), name='detail'),
    path('like/', views.ImageLike.as_view(), name='like'),
    path('ranking/', ImageRanking.as_view(), name='ranking'),
    path('', views.image_list, name='list'),
    path('users_images/', views.users_image_list, name='users_image_list'),
    path('delete/<int:pk>/<slug:slug>/', ImageDelete.as_view(), name="delete_image"),
]
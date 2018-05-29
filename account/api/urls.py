from .views import ProfileDetailRUDView, UserDetailRUDView, UserViewSet, ProfileViewSet

from rest_framework import routers

from django.urls import path, include

router = routers.DefaultRouter()
router.register('profiles', ProfileViewSet)
router.register('users', UserViewSet)

app_name = 'api-accounts'
urlpatterns = [
    path('profile/<int:id>/', ProfileDetailRUDView.as_view(), name='account-detail-rud'),
    path('', include(router.urls)),
    path('user/<int:id>/', UserDetailRUDView.as_view(), name='user-detail-rud'),

]
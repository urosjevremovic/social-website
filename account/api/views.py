from rest_framework import generics, viewsets
from account.models import Profile
from django.contrib.auth.models import User

from .serializers import ProfileSerializer, UserSerializer


class ProfileDetailRUDView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()


class UserDetailRUDView(generics.ListAPIView):
    lookup_field = 'id'
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

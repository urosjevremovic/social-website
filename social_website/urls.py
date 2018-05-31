"""social_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (password_reset, password_reset_done, password_reset_complete,
                                       password_reset_confirm, password_change, password_change_done)
from django.conf import settings
from django.conf.urls.static import static

from account.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name='account'),
    path('images/', include('images.urls', namespace='images')),
    path('password_reset/', password_reset, {'template_name': 'registration/password_reset.html'}, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('password_reset/confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('password_reset/complete/', password_reset_complete, name='password_reset_complete'),
    path('password_change/', password_change, name='password_change'),
    path('password_change/done/', password_change_done, name='password_change_done'),
    path('', dashboard, name='dashboard'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('api/accounts/', include('account.api.urls', namespace='api-accounts')),
    path('api/images/', include('images.api.urls', namespace='api-images')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


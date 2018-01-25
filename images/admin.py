from django.contrib import admin
from .models import Image
# from social_django.models import Association, Nonce, UserSocialAuth
#
# admin.site.unregister(Association)
# admin.site.unregister(Nonce)
# admin.site.unregister(UserSocialAuth)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'image', 'created', ]
    list_filter = ['created']


admin.site.register(Image, ImageAdmin)

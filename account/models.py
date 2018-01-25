from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .utils import code_generator


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', default='users/default_profile_image.png')

    def __str__(self):
        return f"Profile for {self.user.username}"


class Contact(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created', ]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


User.add_to_class('following', models.ManyToManyField('self', through=Contact,
                                                      related_name='followers', symmetrical=False))

User.add_to_class('activation_key', models.CharField(max_length=120, blank=True, null=True))

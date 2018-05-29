from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

from .utils import code_generator
from .models import Profile


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user)
        if not user.is_active:
            user.activation_key = code_generator()
            user.save()
            path = reverse('account:activate', kwargs={"code": user.activation_key})
            full_path = settings.SITE_URL + path
            subject = 'Activate Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {full_path}'
            recipient_list = [user.email]
            html_message = f'<p>Activate your account here: {full_path}</p>'
            sent_mail = send_mail(subject, message, from_email,
                                  recipient_list, fail_silently=False, html_message=html_message)
            return sent_mail


post_save.connect(post_save_user_receiver, sender=User)
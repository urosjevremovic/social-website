from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data.get('url')
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match a valid image extension')
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data.get('url')
        image_name = f'{slugify(image.title)}.{image_url.rsplit(".", 1)[1].lower()}'

        response = request.urlopen(image_url)
        image.image.save(image_name, ContentFile(response.read()), save=False)

        if commit:
            image.save()
        return image


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'description')
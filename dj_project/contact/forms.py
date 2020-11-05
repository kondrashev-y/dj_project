from django import forms
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    """Форма подписки по email"""
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ("name", "email", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "editContent", "placeholder": "Enter your name..."}),
            "email": forms.TextInput(attrs={"class": "editContent", "placeholder": "Enter your email..."})
        }
        labels = {
            "name": '',
            "email": ''

        }

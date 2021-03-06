from django import forms

from .models import Reviews, Rating, RingStar
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control border"}),
            'email': forms.EmailInput(attrs={"class": "form-control border"}),
            'text': forms.Textarea(attrs={"class": "form-control border", 'rows': 3, 'cols': 60})
        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None,
    )

    class Meta:
        model = Rating
        fields = ("star",)

# class AvrgRatingForm(forms.ModelForm):
#     """Форма среднего рейтинга"""
#     avrgstar = forms.ModelChoiceField(
#         queryset=RingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None,
#     )
#
#     class Meta:
#         model = Rating
#         fields = ("avrgstar",)
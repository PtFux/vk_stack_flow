from django import forms
from django.core.exceptions import ValidationError


class ProfileEditForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(
        label="Email Address",
        help_text="A valid email address",
        error_messages={"required": "Please enter your email"}
    )
    upload_avatar = forms.ImageField(required=False)

    def clean(self):
        # валидация всех полей
        return self.cleaned_data

    # def __init__(self, username: str = None, email: str = None, *args, **kwargs):
    #     super(ProfileEditForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['username'].widget.attrs.update({'empty_value': username if username else 'Username'})
    #     self.fields['email'].widget.attrs.update({'empty_value': email if email else 'Email'})
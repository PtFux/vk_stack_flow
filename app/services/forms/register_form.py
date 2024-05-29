import re

from django import forms


class RegisterForm(forms.Form):
    login = forms.CharField()
    email = forms.EmailField(
        label="Email Address",
        help_text="A valid email address",
        error_messages={"required": "Please enter your email"}
    )
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    repeat_password = forms.CharField(widget=forms.PasswordInput, min_length=8,
                                      error_messages={"password_mismatch": "Пароли не совпадают"})
    upload_avatar = forms.ImageField(required=False)

    def clean(self):
        # валидация всех полей
        pass

    def clean_login(self):
        login = self.cleaned_data['login']
        pattern = "^[а-яА-Яa-zA-Z0-9_]+$"
        if not re.match(pattern, login):
            raise forms.ValidationError("Invalid login. Use only letters, numbers and '_'.")
        if not re.match("^[a-zA-ZА-Яа-я][а-яА-Яa-zA-Z0-9_]*$", login):
            raise forms.ValidationError("Login must start with a letter.")
        return login

    def clean_repeat_password(self):
        repeat_password = self.cleaned_data['repeat_password']
        password = self.cleaned_data['password']
        if password != repeat_password:
            raise forms.ValidationError('Passwords do not match', code="password_mismatch")
        return password


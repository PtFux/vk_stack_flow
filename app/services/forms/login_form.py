from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        print(self.cleaned_data)
        super().clean()
        print(self.cleaned_data)
        if not self.errors:
            if self.cleaned_data['username'] == self.cleaned_data['password']:
                raise ValidationError('Username and password match')
        return self.cleaned_data

    def clean_username(self):
        # валидация логина
        login = self.cleaned_data['username']

        # login = clear_(login) # защита от sql инъекций
        # if login == 'test':
        #     print("Login: ", login)
        #     raise ValidationError("Wrong username")
        return login

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == 'test':
            print("Password:", password)
            raise ValidationError("Wrong password")
        return password

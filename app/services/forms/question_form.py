from django import forms


class QuestionForm(forms.Form):
    # login = forms.CharField()
    # email = forms.EmailField(
    #     label="Email Address",
    #     help_text="A valid email address",
    #     error_messages={"required": "Please enter your email"}
    # )
    # password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    # repeat_password = forms.CharField(widget=forms.PasswordInput, min_length=8,
    #                                   error_messages={"password_mismatch": "Пароли не совпадают"})
    # upload_avatar = forms.ImageField(required=False)

    title = forms.CharField(
        max_length=50,
    )

    text = forms.CharField(
        max_length=500,
        widget=forms.Textarea()
    )

    tags = forms.MultipleChoiceField(
        label='Tags',
        help_text="Choose 3 tags",
        widget=forms.CheckboxSelectMultiple
    )

    def clean(self):
        # валидация всех полей
        return self.cleaned_data

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 3:
            raise forms.ValidationError("Too many tags")
        if len(tags) == 0:
            raise forms.ValidationError("No tags")
        return tags

    def clean_title(self):
        title = self.cleaned_data['title']
        # if not title.isalpha():
        #     raise forms.ValidationError("Title must be alphanumeric")
        return title

    def __init__(self, tags: list, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['tags'].choices = tags


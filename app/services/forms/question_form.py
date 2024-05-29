from django import forms
import re


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
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    new_tags = forms.CharField(
        max_length=200,
        widget=forms.Textarea(),
        help_text="Enter tags separated by enter",
        required=False
    )

    def clean(self):
        if self.errors:
            raise forms.ValidationError(f"{self.errors}")
        new_tags = self.cleaned_data['new_tags']
        tags = self.cleaned_data['tags']
        if not (0 < len(new_tags) + len(tags) <= 3):
            raise forms.ValidationError("Tags 0 - 3!!!")
        return self.cleaned_data

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 3:
            raise forms.ValidationError("Too many tags")
        return tags

    def clean_title(self):
        title = self.cleaned_data['title']
        # if not title.isalpha():
        #     raise forms.ValidationError("Title must be alphanumeric")
        return title

    def clean_new_tags(self):
        new_tags = self.cleaned_data['new_tags']
        new_tags = new_tags.split()

        for tag in new_tags:
            if not re.match(r"^[a-zA-ZА-Яа-я][а-яА-Яa-zA-Z0-9_]*$", tag):
                raise forms.ValidationError("Invalid tag")

        return new_tags

    def __init__(self, tags: list, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        self.fields['tags'].choices = tags


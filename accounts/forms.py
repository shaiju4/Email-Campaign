from django import forms
from django.contrib.auth.forms import AuthenticationForm


class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label="Enter a unique username"
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class UserLoginForm(AuthenticationForm):
    pass

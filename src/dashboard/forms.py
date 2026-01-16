from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from api_keys.models import APIKey


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class APIKeyForm(forms.ModelForm):
    class Meta:
        model = APIKey
        fields = [
            "name",
            "plan",
            "expires_at",
            "requests_per_minute",
            "requests_per_day",
            "can_chat_completions",
            "can_embeddings",
            "can_moderations",
            "can_images",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter API key name"}
            ),
            "plan": forms.Select(attrs={"class": "form-control"}),
            "expires_at": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "requests_per_minute": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "requests_per_day": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "can_chat_completions": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "can_embeddings": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "can_moderations": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "can_images": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expires_at"].required = False

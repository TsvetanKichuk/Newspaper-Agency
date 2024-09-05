from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from editorial_office.models import Newspaper, Redactor, Topic


class NewspaperForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "year_of_experience",
            "first_name",
            "last_name",
        )

    def clean_year_of_experience(self):  # this logic is optional, but possible
        return validate_year_of_experience(self.cleaned_data["year_of_experience"])


class RedactorLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["year_of_experience"]

    def clean_year_of_experience(self):
        return validate_year_of_experience(self.cleaned_data["year_of_experience"])


def validate_year_of_experience(
        year_of_experience,
):  # regex validation is also possible here
    if len(year_of_experience) != 0:
        raise ValidationError("should consist more of 0 characters")
    elif not year_of_experience.isdigit():
        raise ValidationError("characters should be digits")

    return year_of_experience


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by title"
            }
        ),
    )


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by username"
            }
        ),
    )


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "search by name"
            }
        ),
    )

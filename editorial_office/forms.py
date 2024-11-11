from django import forms
from django.contrib.auth.forms import UserCreationForm

from editorial_office.models import Newspaper, Redactor, Topic


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=Redactor.objects.all(),
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


class RedactorYearsOfExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "year_of_experience",
            "first_name",
            "last_name",
        )


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
    publishers = forms.CharField(
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

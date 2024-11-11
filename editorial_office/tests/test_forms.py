from django.test import TestCase
from editorial_office.forms import RedactorCreationForm, RedactorYearsOfExperienceUpdateForm
from editorial_office.models import Redactor


class RedactorCreationFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "redactoruser",
            "password1": "Password123!",
            "password2": "Password123!",
            "year_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_redactor_creation_form_valid(self):
        form = RedactorCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form_invalid_password_mismatch(self):
        data = self.valid_data.copy()
        data["password2"] = "AnotherPassword123!"
        form = RedactorCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_redactor_creation_form_missing_field(self):
        data = self.valid_data.copy()
        del data["year_of_experience"]
        form = RedactorCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("year_of_experience", form.errors)


class RedactorYearsOfExperienceUpdateFormTest(TestCase):
    def setUp(self):
        self.redactor = Redactor.objects.create(
            username="redactoruser",
            year_of_experience=5,
            first_name="John",
            last_name="Doe"
        )
        self.valid_data = {
            "username": "redactoruser",
            "year_of_experience": 7,
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_redactor_years_of_experience_update_form_valid(self):
        form = RedactorYearsOfExperienceUpdateForm(data=self.valid_data, instance=self.redactor)
        self.assertTrue(form.is_valid())

    def test_redactor_years_of_experience_update_form_invalid(self):
        data = self.valid_data.copy()
        data["year_of_experience"] = -1
        form = RedactorYearsOfExperienceUpdateForm(data=data, instance=self.redactor)
        self.assertFalse(form.is_valid())
        self.assertIn("year_of_experience", form.errors)

    def test_redactor_update_form_missing_last_name(self):
        data = self.valid_data.copy()
        del data["last_name"]
        form = RedactorYearsOfExperienceUpdateForm(data=data, instance=self.redactor)
        self.assertFalse(form.is_valid())
        self.assertIn("last_name", form.errors)

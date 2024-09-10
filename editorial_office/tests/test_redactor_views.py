from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from editorial_office.forms import NewspaperSearchForm
from editorial_office.models import Redactor, Newspaper, Topic


class ToggleAssignToNewspapersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Redactor.objects.create(username=self.client)
        self.topic = Topic.objects.create(
            name="Test Manufacturer"
        )

        self.newspaper = Newspaper.objects.create(
            title="Test Newsapers",
            topic=self.topic
        )
        self.client.login(username="testuser", password="12345")
        self.client.force_login(self.user)

    def test_toggle_assign_to_newspapers_add(self):
        response = self.client.post(
            reverse("editorial_office:toggle-newspaper-assign", args=[self.newspaper.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("editorial_office:newspaper-detail",
                    args=[self.newspaper.id])
        )
        self.assertIn(self.newspaper, self.user.newspapers.all())

    def test_toggle_assign_to_newspapers_remove(self):
        self.user.newspapers.add(self.newspaper)
        response = self.client.post(
            reverse("editorial_office:toggle-newspaper-assign",
                    args=[self.newspaper.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("editorial_office:newspaper-detail",
                    args=[self.newspaper.id])
        )

        self.assertNotIn(self.newspaper, self.user.newspapers.all())


class NewspapersListViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            password="testpass",
            year_of_experience="7"
        )
        self.client.force_login(self.user)

    def test_redactor_view_url_exists_at_desired_location(self):
        response = self.client.get("/redactor/")
        self.assertEqual(response.status_code, 200)

    def test_redactor_view_uses_correct_template(self):
        response = self.client.get(reverse("editorial_office:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editorial_office/redactor_list.html")

    def test_lists_all_redactors(self):
        response = self.client.get(reverse("editorial_office:redactor-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactors_list"]), 1)

    def test_redactor_search_functionality(self):
        response = self.client.get(
            reverse("editorial_office:redactor-list")
            + "?username=testuser"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactors_list"]), 1)
        self.assertEqual(
            response.context["redactors_list"][0].username,
            "testuser"
        )

    def test_redactor_invalid_search_form(self):
        response = self.client.get(reverse("editorial_office:redactor-list") + "?username=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactors_list"]), 1)

    def test_get_queryset_with_redactor_username(self):
        response = self.client.get("/redactor/?username=testuser")
        queryset = response.context["redactors_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].username, "testuser")

    def test_redactor_search_case_insensitive(self):
        response = self.client.get("/redactor/?model=TEST USER")
        self.assertEqual(len(response.context["redactors_list"]), 1)

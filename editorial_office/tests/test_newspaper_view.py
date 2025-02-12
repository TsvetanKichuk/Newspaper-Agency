from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from editorial_office.models import Topic, Newspaper


class NewspaperListViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

        self.user = self.User.objects.create_user(
            username="testuser",
            password="testpass"
        )
        topic = Topic.objects.create(name="TestTopic")
        Newspaper.objects.create(title="TestTitle", topic=topic,)
        self.client.login(username="testuser", password="testpass")

    def test_newspaper_view_url_exists_at_desired_location(self):
        response = self.client.get("/newspapers/")
        self.assertEqual(response.status_code, 200)

    def test_newspaper_view_uses_correct_template(self):
        response = self.client.get(reverse("editorial_office:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editorial_office/newspaper_list.html")

    def test_lists_all_newspapers(self):
        response = self.client.get(reverse("editorial_office:newspaper-list") + "?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)

    def test_newspaper_search_functionality(self):
        response = self.client.get(
            reverse("editorial_office:newspaper-list") + "?model=Test title"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)
        self.assertEqual(response.context["newspaper_list"][0].title, "TestTitle")

    def test_invalid_newspaper_search_form(self):
        response = self.client.get(reverse("editorial_office:newspaper-list") + "?model=")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)

    def test_get_queryset_with_newspaper_model(self):
        response = self.client.get("/newspapers/?model=Test title")
        queryset = response.context["newspaper_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].title, "TestTitle")

    def test_newspaper_search_case_insensitive(self):
        response = self.client.get("/newspapers/?model=TEST TITLE")
        self.assertEqual(len(response.context["newspaper_list"]), 1)

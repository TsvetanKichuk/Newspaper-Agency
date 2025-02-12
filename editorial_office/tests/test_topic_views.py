from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from editorial_office.models import Topic


class TopicListViewTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        Topic.objects.create(name="Test1")
        Topic.objects.create(name="Test2")
        Topic.objects.create(name="Test3")
        self.client.login(username="testuser", password="testpass")

    def test_topics_view_url_exists_at_desired_location(self):
        response = self.client.get("/topics/")
        self.assertEqual(response.status_code, 200)

    def test_topics_view_uses_correct_template(self):
        response = self.client.get(reverse("editorial_office:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editorial_office/topic_list.html")

    def test_lists_all_topics(self):
        response = self.client.get(
            reverse("editorial_office:topic-list")
            + "?page=1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 3)

    def test_topics_search_functionality(self):
        response = self.client.get(
            reverse("editorial_office:topic-list")
            + "?name=Test1"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 1)
        self.assertEqual(
            response.context["topic_list"][0].name,
            "Test1"
        )

    def test_topics_invalid_search_form(self):
        response = self.client.get(
            reverse("editorial_office:topic-list")
            + "?name="
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 3)

    def test_get_queryset_with_topic_name(self):
        response = self.client.get("/topics/?name=Test1")
        queryset = response.context["topic_list"]

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(queryset[0].name, "Test1")

    def test_topics_search_case_insensitive(self):
        response = self.client.get("/topics/?name=Test2")
        self.assertEqual(len(response.context["topic_list"]), 1)

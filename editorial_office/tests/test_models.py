from django.contrib.auth import get_user_model
from django.test import TestCase

from editorial_office.models import Topic, Newspaper


class ModelTests(TestCase):
    def test_topic_str(self):
        topic = Topic.objects.create(name="test name")
        self.assertEqual(str(topic), f"{topic.name}")

    def test_newspapers_str(self):
        topic = Topic.objects.create(name="test topic")
        newspapers = Newspaper.objects.create(title="Test", topic=topic)
        self.assertEqual(str(newspapers), f"{newspapers.title} ({newspapers.published_date})")

    def test_driver_str(self):
        redactor = get_user_model().objects.create(
            username="test username",
            password="test123",
            first_name="test_first",
            last_name="test_last",
        )
        self.assertEqual(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
        )

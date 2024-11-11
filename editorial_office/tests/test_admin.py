from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123",
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="test_redactor",
            password="testpass",
            year_of_experience="0"

        )

    def test_redactor_experience_list_display(self):
        """
        test that driver's license number is in list_display on admin page
        :return:
        """
        url = reverse("admin:editorial_office_redactor_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.redactor.year_of_experience)

    def test_fieldsets(self):
        """
                test that driver's additional info
                is in list_display on admin page
                :return:
                """
        url = reverse("admin:editorial_office_redactor_change", args=[self.redactor.id])
        res = self.client.get(url)
        self.assertContains(res, self.redactor.year_of_experience)

    def test_add_fieldsets(self):
        """
                test that driver's additional info
                is added in list_display on admin page
                :return:
                """
        url = reverse("admin:editorial_office_redactor_add")
        res = self.client.get(url)
        self.assertContains(res, self.redactor.id)

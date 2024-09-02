from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "publisher"
        verbose_name_plural = "publishers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("editorial_office:publisher-detail", kwargs={"pk": self.pk})


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=2000)
    published_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(Redactor, related_name="newspapers", blank=True)

    def __str__(self):
        return f"{self.title} ({self.published_date})"


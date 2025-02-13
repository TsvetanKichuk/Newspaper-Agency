from django.urls import path
from django.views.generic import TemplateView

from editorial_office.views import (
    index,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    RedactorListView,
    RedactorDetailView,
    RedactorCreateView,
    RedactorUpdateView,
    RedactorDeleteView,
    TopicListView,
    TopicCreateView,
    TopicUpdateView,
    TopicDeleteView,
    toggle_assign_to_newspaper,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "topics/",
        TopicListView.as_view(),
        name="topic-list",
    ),
    path(
        "topics/create/",
        TopicCreateView.as_view(),
        name="topic-create",
    ),
    path(
        "topics/<int:pk>/update/",
        TopicUpdateView.as_view(),
        name="topic-update",
    ),
    path(
        "topics/<int:pk>/delete/",
        TopicDeleteView.as_view(),
        name="topic-delete",
    ),
    path("newspapers/", NewspaperListView.as_view(), name="newspaper-list"),
    path("newspapers/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspapers/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspapers/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspapers/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path(
        "newspapers/<int:pk>/toggle-assign/",
        toggle_assign_to_newspaper,
        name="toggle-newspaper-assign",
    ),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path(
        "redactor/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"
    ),
    path("redactor/", RedactorListView.as_view(), name="redactor-list"),
    path(
        "redactor/<int:pk>/", RedactorDetailView.as_view(), name="redactor-detail"
    ),
    path("redactor/create/", RedactorCreateView.as_view(), name="redactor-create"),
    path(
        "redactor/<int:pk>/update/",
        RedactorUpdateView.as_view(),
        name="redactor-update",
    ),
    path(
        "redactor/<int:pk>/delete/",
        RedactorDeleteView.as_view(),
        name="redactor-delete",
    ),
    path("", TemplateView.as_view(template_name="editorial_office/index.html"), name="index"),
]

app_name = "editorial_office"

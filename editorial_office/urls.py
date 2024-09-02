from django.urls import path

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
    RedactorLicenseUpdateView,
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
        name="toggle-car-assign",
    ),
    path("publishers/", RedactorListView.as_view(), name="publisher-list"),
    path(
        "publishers/<int:pk>/", RedactorDetailView.as_view(), name="publisher-detail"
    ),
    path("publishers/", RedactorListView.as_view(), name="publisher-list"),
    path(
        "publishers/<int:pk>/", RedactorDetailView.as_view(), name="publisher-detail"
    ),
    path("publishers/create/", RedactorCreateView.as_view(), name="publisher-create"),
    path(
        "publishers/<int:pk>/update/",
        RedactorLicenseUpdateView.as_view(),
        name="publisher-update",
    ),
    path(
        "publisher/<int:pk>/delete/",
        RedactorDeleteView.as_view(),
        name="publisher-delete",
    ),
]

app_name = "editorial_office"

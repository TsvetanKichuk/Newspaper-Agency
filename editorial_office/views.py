from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from editorial_office.forms import (
    RedactorYearsOfExperienceUpdateForm,
    RedactorCreationForm,
    RedactorSearchForm,
    NewspaperSearchForm,
    TopicSearchForm,
    NewspaperForm,
)
from editorial_office.models import Redactor, Newspaper, Topic


@login_required
def index(request):
    """View function for the home page of the site."""

    num_publishers = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_publishers": num_publishers,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
        "num_visits": num_visits + 1,
    }

    return render(request, "editorial_office/index.html", context=context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "editorial_office/topic_list.html"
    paginate_by = 2
    queryset = Topic.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        context["search_form"] = TopicSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = TopicSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("editorial_office:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("editorial_office:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("editorial_office:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    paginate_by = 1
    queryset = Newspaper.objects.select_related("topic")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        title = self.request.GET.get("title")

        if title:
            return self.queryset.filter(title__icontains=title)

        return self.queryset


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("editorial_office:newspaper-list")
    queryset = Newspaper.objects.all().select_related("topic")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("editorial_office:newspaper-list")
    queryset = Newspaper.objects.all().select_related("topic")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("editorial_office:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 5
    context_object_name = "redactors_list"
    queryset = Redactor.objects.all().prefetch_related("newspapers__topic")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)

        username = self.request.GET.get("username", "")

        context["search_form"] = RedactorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        username = self.request.GET.get("username")

        if username:
            return self.queryset.filter(username__icontains=username)

        return self.queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related("newspapers")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorYearsOfExperienceUpdateForm
    success_url = reverse_lazy("editorial_office:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("")


@login_required
def toggle_assign_to_newspaper(request, pk):
    publisher = Redactor.objects.get(id=request.user.id)
    if (
            Newspaper.objects.get(id=pk) in publisher.newspapers.all()
    ):
        publisher.newspapers.remove(pk)
    else:
        publisher.newspapers.add(pk)
    return HttpResponseRedirect(reverse_lazy("editorial_office:newspaper-detail", args=[pk]))

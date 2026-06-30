from celery.app.log import TaskFormatter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from rest_framework.reverse import reverse_lazy
from django.urls import reverse_lazy

from devboard.forms import TaskForm, ProjectForm
from devboard.models import Project, Task

from django.db.models import Count

from django.utils.translation import gettext_lazy as _


# def index(request):
#     return HttpResponse("<h1>Devboard - etap 1: scaffold!</h1>")

# def index(request):
#     return render(request, "index.html")
#


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "devboard/project_list.html"
    context_object_name = "projects"


    def get_queryset(self):
#        try:
        return (
            Project.objects.filter(owner=self.request.user)
            .annotate(task_count=Count("tasks"))
            .order_by("-created_at")
        )

#        except TypeError:
#            return None


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "devboard/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["tasks"] = (
            self.object.tasks
            .select_related("assignee")
            .order_by("-priority", "due_date")
        )
        return ctx
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "devboard/task_create.html"
    form_class = TaskForm
    success_url = reverse_lazy("devboard:lista-project")

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", args=[self.object.project.id])

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["project"].queryset = Project.objects.filter(owner=self.request.user)
        return form

    def form_valid(self, form):
        #messages.success(self.request, _(f"Zadanie '{form.instance.title}' zostało utworzone."))
        messages.success(self.request, _(f"Zadanie zostało utworzone."))

        return super().form_valid(form)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "devboard/project_create.html"
    form_class = ProjectForm
    success_url = reverse_lazy("devboard:lista-project")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Projekt '{form.instance.name}' został utworzony.")
        return super().form_valid(form)

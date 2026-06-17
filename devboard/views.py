from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from devboard.models import Project

from django.db.models import Count
# def index(request):
#     return HttpResponse("<h1>Devboard - etap 1: scaffold!</h1>")

# def index(request):
#     return render(request, "index.html")
#


class ProjectListView(ListView, LoginRequiredMixin):
    model = Project
    template_name = "devboard/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return (
            Project.objects.filter(owner=self.request.user)
            .annotate(task_count=Count("tasks"))
            .order_by("-created_at")
        )

class ProjectDetailView(DetailView,LoginRequiredMixin):
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

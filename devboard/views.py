from celery.app.log import TaskFormatter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View

from django.shortcuts import redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from rest_framework.reverse import reverse_lazy
from django.urls import reverse_lazy

from devboard.forms import TaskForm, ProjectForm
from devboard.models import Project, Task

from django.db.models import Count, Q

from django.utils.translation import gettext_lazy as _


from devboard.mixins import OwnerQuerysetMixin


# def index(request):
#     return HttpResponse("<h1>Devboard - etap 1: scaffold!</h1>")

# def index(request):
#     return render(request, "index.html")
#


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "devboard/project_list.html"
    context_object_name = "projects"


#    def get_queryset(self):
#        try:
#         return (
#             Project.objects.filter(owner=self.request.user)
#             .annotate(task_count=Count("tasks"))
#             .order_by("-created_at")
#         )


    def get_queryset(self):
        return (
            super().get_queryset()
            .annotate(task_count=Count("tasks"))
            .order_by("-created_at")
        )
#        except TypeError:
#            return None


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "devboard/project_detail.html"
    context_object_name = "project"

 #   def get_queryset(self):
 #       return Project.objects.filter(owner=self.request.user)

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


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "devboard/task_create.html"
    form_class = TaskForm
    owner_field = "project__owner"

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", args=[self.object.project.id])
    #
    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)
    #     form.fields["project"].queryset = Project.objects.filter(owner=self.request.user)
    #     return form
    #
    # def form_valid(self, form):
    #     messages.success(self.request, _(f"Zadanie '{form.instance.title}' zostało zaktualizowane."))
    #     return super().form_valid(form)

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = "devboard/project_create.html"
    form_class = ProjectForm
    success_url = reverse_lazy("devboard:lista-project")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f"Projekt '{form.instance.name}' został utworzony.")
        return super().form_valid(form)

# class TaskDeleteView(LoginRequiredMixin, DeleteView):
#     model = Task
#     template_name = "devboard/task_confirm_delete.html"
#     #form_class = TaskForm
#     success_url = reverse_lazy("devboard:lista-project")
#
#     def get_success_url(self):
#         return reverse_lazy("devboard:project-detail", args=[self.object.project.id])


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "devboard/task_confirm_delete.html"
    owner_field = "project__owner"

    def get_success_url(self):
        return reverse_lazy("devboard:project-detail", args=[self.object.project.id])


class TaskStatusUpdateView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        q_owner = Q(project__owner=self.request.user)
        q_assignee = Q(assignee=self.request.user)
        qs = Task.objects.filter(q_owner | q_assignee).filter(pk=self.kwargs["pk"])
        task = get_object_or_404(qs)
        new_status = request.POST.get("status")
        if not new_status or new_status not in Task.Status.values:
            raise BadRequest("Missing or incorrect new status")
            # return HttpResponseBadRequest("Missing or incorrect new status")
        task.status = new_status
        task.save()
        messages.success(request, "Status zaktualizowany")
        return redirect("devboard:project-detail", pk=task.project.pk)
#
# class TaskStatusUpdateView(LoginRequiredMixin, View):
#     http_method_names = []
#     # # model = Task
#     # # template_name = "devboard/task_status_update.html"
#     # # fields = ["status"]
#     # # owner_field = "project__owner"
#     #
#     # def get_success_url(self):
#     #     return reverse_lazy("devboard:project-detail", args=[self.object.project.id])
#
#     def post(self, request, *args, **kwargs):
#         #qs = Task.objects.filter(pk= self.kwargs["pk"]) #... # pk taska: self.kwargs["pk"]
#         q_owner = Q(project__owner=self.request.user)
#         q_assignee = Q(assignee=self.request.user)
#         qs = Task.objects.filter(q_owner | q_assignee).filter(pk=self.kwargs["pk"]) #... # pk taska: self.kwargs["pk"])
#         #qs = Task.objects.filter(pk= self.kwargs["pk"]) #... # pk taska: self.kwargs["pk"]
#
#         task = get_object_or_404(qs)
#         new_status = request.POST.get("status")
#         if not new_status or new_status not in Task.Status.values:
#             raise BadRequest("Missing or incorrect new status")
#             return HttpResponseBadRequest("Missing or incorrect new status")
#         # zweryfikować new_status
#         task.status = new_status
#         task.save()
#         messages.success(request, f"Status zadania '{task.title}' został zaktualizowany.")
#
#         return redirect("devboard:project-detail", pk=task.project.pk)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "devboard/task_detail.html"
    context_object_name = "task"

 #   def get_queryset(self):
 #       return Task.objects.filter(owner=self.request.user)

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #     ctx["tasks"] = (
    #         self.object.tasks
    #         .select_related("assignee")
    #         .order_by("-priority", "due_date")
    #     )
    #     return ctx
    #

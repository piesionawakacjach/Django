from click import clear
from django import forms

from devboard.models import Task, Project


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "project", "assignee", "priority", "due_date", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "project": forms.Select(attrs={"class": "form-control"}),
            "assignee": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),

        }

    def clean(self):
        cleaned = super().clean()
        priority = cleaned.get("priority")
        due_date = cleaned.get("due_date")
        if priority == Task.Priority.HIGH and not due_date:
            raise forms.ValidationError("Zadanie o wysokim priorytecie musi mieć ustawiony termin wykonania.")
        return cleaned


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),
        }

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa")
    description = models.TextField(blank=True, verbose_name="Opis")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Właściciel",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Projekt"
        verbose_name_plural = "Projekty"

    def __str__(self) -> str:
        return self.name

    def task_count(self) -> int:
        return self.tasks.count()


class Task(models.Model):
    """Zadanie przypisane do projektu."""

    class Status(models.TextChoices):
        TODO = "TODO",                  _("Do zrobienia")
        IN_PROGRESS = "IN_PROGRESS",    _("W trakcie")
        DONE = "DONE",                  _("Ukończone")

    class Priority(models.IntegerChoices):
        LOW = 1,    _("Niski")
        MEDIUM = 2, _("Średni")
        HIGH = 3,   _("Wysoki")

    title = models.CharField(max_length=300, verbose_name=_("Tytuł"))
    description = models.TextField(blank=True, verbose_name=_("Opis"))
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Projekt",
    )
    assignee = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_tasks",
        verbose_name="Przypisany do",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
        verbose_name="Status",
    )
    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Priorytet",
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Termin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-priority", "due_date"]
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"

    def __str__(self) -> str:
        return f"[{self.get_priority_display()}] {self.title}"

    @property
    def is_overdue(self) -> bool:
        if self.due_date and self.status != self.Status.DONE:
            return self.due_date < timezone.now().date()
        return False


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Zadanie",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Autor",
    )
    body = models.TextField(verbose_name="Treść")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"

    def __str__(self) -> str:
        return f"{self.author.username} @ {self.task.title[:40]}"

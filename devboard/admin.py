from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Task, Comment

# admin.site.register(Project)
#admin.site.register(Task)
admin.site.register(Comment)


class TaskInline(admin.TabularInline):
    """Zadania wyświetlane wewnątrz projektu."""
    model = Task
    fields = ("title", "status", "priority", "assignee", "due_date")
    extra = 1
    show_change_link = True

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name","owner", "created_at", "task_count")
    search_fields = ("name", "description")
    list_filter = ("name", "created_at")
    inlines = [TaskInline]

    @admin.display(description="Zadań")
    def task_count(self, obj):
        return obj.tasks.count()
        return format('<b>{}</b>'.format(count))

# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ("title", "is_overdue", "description", "project", "assignee", "status", "priority", "due_date", "created_at", "updated_at")
#     search_fields = ("title",)
#     list_filter = ("due_date", "created_at", "updated_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title", "status_badge", "status", "project", "priority",
        "assignee", "due_date",
    )
    list_filter = ("status", "priority", "project", "assignee")
    search_fields = ("title", "description")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "description", "project")}),
        ("Przypisanie", {"fields": ("assignee", "due_date")}),
        ("Status", {"fields": ("status", "priority")}),
        ("Metadane", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            "TODO": "#6c757d",
            "IN_PROGRESS": "#0d6efd",
            "DONE": "#198754",
        }
        color = colors.get(obj.status, "#000")
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:4px">{}</span>',
            color, obj.get_status_display(),
        )

admin.site.site_header = "DevBoard - Panel Administracyjny"

admin.site.site_title = "DevBoard Admin"
admin.site.index_title = "Zarządzanie projektem"

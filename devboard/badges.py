from django.utils.html import format_html

STATUS_COLORS = {
    "TODO": "dark",
    "IN_PROGRESS": "info",
    "DONE": "success",
}

STATUS_ICONS = {
    "TODO": "circle",
    "IN_PROGRESS": "hourglass-split",
    "DONE": "check-circle",
}


def render_status_badge(task):
    return format_html(
        '<span class="badge bg-{}"><i class="bi bi-{}"></i> {}</span>',
        STATUS_COLORS[task.status],
        STATUS_ICONS[task.status],
        task.get_status_display(),
    )
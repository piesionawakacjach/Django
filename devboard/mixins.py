
from django.contrib.auth.mixins import LoginRequiredMixin
from devboard.models import Project

class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
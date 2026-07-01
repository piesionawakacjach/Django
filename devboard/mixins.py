
from django.contrib.auth.mixins import LoginRequiredMixin
from devboard.models import Project

class OwnerQuerysetMixin(LoginRequiredMixin):
    owner_field = "owner"

    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})
#        return Project.objects.filter(owner=self.request.user)
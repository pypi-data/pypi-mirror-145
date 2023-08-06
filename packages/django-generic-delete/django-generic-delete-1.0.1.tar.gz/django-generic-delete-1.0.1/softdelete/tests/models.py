from django.db import models
from django.utils.timezone import now

from softdelete.models import SoftDeletionModel


class TestModel(SoftDeletionModel):
    title = models.CharField(blank=True, null=True, max_length=1000)
    created_at = models.DateTimeField(auto_created=True, default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

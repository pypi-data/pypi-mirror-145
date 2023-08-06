from django.db import models
from django.utils.timezone import now


class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    class Meta:
        abstract = True

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    deleted_at = models.DateTimeField(blank=True, null=True)

    def delete(self, using=None, keep_parents=False):
        if self.deleted_at:
            raise ValueError('This object had deleted before')
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()

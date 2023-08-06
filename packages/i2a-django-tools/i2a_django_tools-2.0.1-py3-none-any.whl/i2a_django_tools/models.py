from django.db import models, transaction
from django.db.transaction import atomic
from django.utils import timezone

LIVE_REVISION_ID = 2147483647  # max postgresql integer value (2 ** 31 - 1)


class CreateTimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Revision(CreateTimeStampedModel):

    @property
    def is_live(self):
        return self.id == LIVE_REVISION_ID

    def __str__(self):
        if self.is_live:
            return "LIVE"
        else:
            return "@{}".format(self.created_at.isoformat(' '))


def get_live_revision():
    Revision.objects.get_or_create(id=LIVE_REVISION_ID)
    return LIVE_REVISION_ID


class UpdateCreateTimeStampedModel(CreateTimeStampedModel):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ArchiveQuerySet(models.QuerySet):

    def non_archived(self):
        return self.filter(archive_revision_id=LIVE_REVISION_ID)

    def published(self):
        return self.non_archived()

    def archived(self):
        return self.exclude(archive_revision_id=LIVE_REVISION_ID)

    def restore(self):
        for item in self.all():
            item.restore()

    @atomic
    def archive(self, revision=None, use_signals=False):
        if not revision:
            revision = Revision.objects.create()
        if use_signals:
            for item in self.all():
                item.archive(revision)
        else:
            self.published().update(
                archive_revision=revision
            )


class ArchiveModel(UpdateCreateTimeStampedModel):
    objects = ArchiveQuerySet.as_manager()
    archive_revision = models.ForeignKey(
        Revision, default=get_live_revision,
        on_delete=models.SET_DEFAULT
    )
    archived_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def is_archived(self):
        return self.archive_revision_id != LIVE_REVISION_ID

    @property
    def is_active(self):
        return self.archive_revision_id == LIVE_REVISION_ID

    def archive(self, revision=None):
        with transaction.atomic():
            if not revision:
                revision = Revision.objects.create()
            self.archive_revision = revision
            self.archived_at = timezone.now()
            self.save()

    def restore(self):
        self.archive_revision_id = get_live_revision()
        self.save()

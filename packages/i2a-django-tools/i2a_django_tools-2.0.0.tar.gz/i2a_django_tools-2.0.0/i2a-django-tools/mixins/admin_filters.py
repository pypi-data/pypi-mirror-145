from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from models import LIVE_REVISION_ID


class IsArchivedListFilter(SimpleListFilter):
    title = _('is archived.')

    parameter_name = 'archive_revision'

    def lookups(self, request, model_admin):
        return (
            ('Is Live', _('Is Live.')),
            ('Is Archived', _('Is Archived.')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'LIVE':
            return queryset.filter(archive_revision=LIVE_REVISION_ID)
        if self.value() == 'Archived':
            return queryset.filter(~Q(archive_revision=LIVE_REVISION_ID))

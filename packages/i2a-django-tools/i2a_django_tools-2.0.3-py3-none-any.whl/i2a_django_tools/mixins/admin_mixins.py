
class AdminArchiveModelMixin:

    def make_published(self, request, queryset):
        for obj in queryset:
            obj.restore()

    def make_archived(self, request, queryset):
        for obj in queryset:
            obj.archive()

    make_published.short_description = "Mark selected objects as LIVE"
    make_archived.short_description = "Mark selected objects as ARCHIVE"
    make_published.allowed_permissions = ('change',)
    make_archived.allowed_permissions = ('change',)

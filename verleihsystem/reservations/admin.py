from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from reservations.models import Reservation, ReservationEntry


def mark_acknowledged(modeladmin, request, queryset):
    queryset.update(state=1)
mark_acknowledged.short_description = _("Mark selected reservations as acknowledged")


def mark_rejected(modeladmin, request, queryset):
    queryset.update(state=2)
mark_rejected.short_description = _("Mark selected reservations as rejected")


class ReservationItemInline(admin.TabularInline):
    model = ReservationEntry
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    list_filter = ('state','start_date', 'end_date',)
    date_hierarchy = 'timestamp'
    list_display = ('user', 'start_date', 'end_date', 'state',)
    list_editable = ('state',)
    actions = [mark_acknowledged, mark_rejected]
    inlines = [
        ReservationItemInline,
    ]


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationEntry)

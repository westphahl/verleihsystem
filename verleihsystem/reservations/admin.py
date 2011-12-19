from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from reservations.models import Reservation, ReservationEntry, \
    AdminReservationEntry


def mark_acknowledged(modeladmin, request, queryset):
    """
    Custom admin command for acknowledging all selected reservations.
    """
    queryset.update(state=1)
    # We have to create the resevation ticket and notify the user manually,
    # since the save() method is NOT called when executing admin commands.
    [(e.create_pdf(), e.notify_user()) for e in queryset]
mark_acknowledged.short_description = _("Mark selected reservations as acknowledged")


def mark_rejected(modeladmin, request, queryset):
    """
    Custom admin command for rejecting all selected reservations.
    """
    queryset.update(state=2)
    # We have to  notify the user manually, since the save() method is NOT
    # called when executing admin commands.
    [e.notify_user() for e in queryset]
mark_rejected.short_description = _("Mark selected reservations as rejected")


class ReservationItemInline(admin.TabularInline):
    """
    Inline for editing reservation items on the reservation admin page.
    """
    model = ReservationEntry
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    """
    Admin for the reservation model.
    """
    list_filter = ('state','start_date', 'end_date',)
    date_hierarchy = 'timestamp'
    list_display = ('user', 'start_date', 'end_date', 'state',)
    list_editable = ('state',)
    actions = [mark_acknowledged, mark_rejected]
    inlines = [
        ReservationItemInline,
    ]


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(AdminReservationEntry)

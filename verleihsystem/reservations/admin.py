from django.contrib import admin

from reservations.models import Reservation, ReservationEntry


class ReservationItemInline(admin.TabularInline):
    model = ReservationEntry
    extra = 0


class ReservationAdmin(admin.ModelAdmin):
    list_filter = ('confirmed','start_date', 'end_date',)
    date_hierarchy = 'timestamp'
    list_display = ('user', 'start_date', 'end_date', 'confirmed',)
    list_editable = ('confirmed',)
    inlines = [
        ReservationItemInline,
    ]


admin.site.register(Reservation, ReservationAdmin)
admin.site.register(ReservationEntry)

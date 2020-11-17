from django.contrib import admin

from .models import ConferenceRoom


@admin.register(ConferenceRoom)
class ConferenceRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'manager',)
    list_filter = ('manager',)
    search_fields = ('name', 'address',)
    readonly_fields = ()
    fieldsets = [
        ('Conference Room Information', {'fields': ('name',
                                                    'manager',
                                                    'address',)}),
    ]

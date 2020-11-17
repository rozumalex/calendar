from django.contrib import admin

from .models import Meeting, Participant


class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 0


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'owner', 'start', 'end', 'location',)
    list_filter = ('owner', 'location',)
    search_fields = ('event_name', 'description',)
    readonly_fields = ()
    fieldsets = [
        ('General Information', {'fields': ('event_name',
                                            'meeting_agenda',)}),
        ('Location Information', {'fields': ('start', 'end', 'location',)}),
    ]
    inlines = (ParticipantInline,)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

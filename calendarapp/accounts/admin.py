from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'timezone',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    search_fields = ('first_name', 'last_name', 'username', 'email',)
    readonly_fields = ('date_joined', 'last_login',)
    fieldsets = [
        ('Account Information', {'fields': ('username',
                                            'email',
                                            'date_joined',
                                            'last_login',)}),
        ('Personal Information', {'fields': ('first_name',
                                             'last_name',)}),
        ('Account Settings', {'fields': (('timezone',),)}),
        ('Access Settings', {'fields': (('is_active',
                                         'is_staff',
                                         'is_superuser',),)}),
    ]

'admin for phone models'
from django.contrib import admin

from .models import ClientCall

class ClientCallAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Input', {
            'fields': ('client_name', 'location_name', 'bed_count'),
        }),
        ('Outcome', {
            'fields': ('shelter',)
        }),
        ('Meta', {
            'fields': ('sid', 'call_state'),
        }),
    )
    readonly_fields = ('call_state',)

    list_display = ('sid', 'updated_at', 'call_state', 'bed_count')

admin.site.register(ClientCall, ClientCallAdmin)

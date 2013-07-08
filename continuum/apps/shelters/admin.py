'admin for shelter models'
from django.contrib import admin

from .models import Shelter, Availability

class ShelterAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'phone_number')
        }),
        ('Filtering', {
            'fields': ('classifier_action',),
            'classes': ['collapse'],
        }),
        ('Location', {
            'fields': (('latitude', 'longitude'),),
            'classes': ['collapse'],
        })
    )

    list_display = ('name', 'address', 'phone_number')
    search_fields = ('name', 'address', 'phone_number')

admin.site.register(Shelter, ShelterAdmin)

admin.site.register(Availability)

from django.contrib import admin
from .models import Station

class StationAdmin(admin.ModelAdmin):
    list_display = ('station_id', 'station_name', 'location', 'station_type', 'status')
    search_fields = ('station_id', 'station_name', 'location')
    list_filter = ('station_type', 'status')

admin.site.register(Station, StationAdmin)

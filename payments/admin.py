from django.contrib import admin
from .models import Plan  # Import the Plan model

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'devices', 'validity')  # Display columns in admin panel
    search_fields = ('name', 'duration', 'validity')  # Enable search functionality
    list_filter = ('duration', 'validity')  # Add filters

# Alternative way without decorator:
# admin.site.register(Plan, PlanAdmin)
from django.contrib import admin
from .models import MpesaTransaction

@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan_name", "phone_number", "amount", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("phone_number", "plan_name", "user__username")
    ordering = ("-created_at",)

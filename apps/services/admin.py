from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('business', 'service_name', 'description', 'duration_minutes', 'price', 'status', 'created_at', 'updated_at')

# Register your models here.

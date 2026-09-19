from django.contrib import admin
from apps.appointment_service.models import AppointmentService

@admin.register(AppointmentService)
class AppointmentServiceAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'service', 'created_at', 'updated_at')

# Register your models here.

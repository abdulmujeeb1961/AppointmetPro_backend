from django.contrib import admin
from apps.Appointment.models import Appointment

@admin.register(Appointment)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_code', 'customer', 'appointment_date', 'booking_source', 'status')  # Register your models here.

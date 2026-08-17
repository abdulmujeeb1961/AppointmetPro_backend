from django.contrib import admin
from .models import WorkingHours
@admin.register(WorkingHours)

class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('staff', 'day_of_week', 'start_time', 'end_time', 'is_working_day')
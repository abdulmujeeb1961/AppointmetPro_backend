from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('holiday_name', 'holiday_date', 'holiday_type', 'is_full_day', 'start_time', 'end_time', 'notes', 'created_at', 'updated_at')   
    
    
   
# Register your models here.

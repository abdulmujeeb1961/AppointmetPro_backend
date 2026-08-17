from django.contrib import admin
from .models import Staff

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_code', 'first_name', 'last_name', 'email', 'mobile_number', 'designation', 'gender', 'joining_date', 'experience_years', 'profile_photo', 'status', 'created_at', 'updated_at')

# Register your models here.

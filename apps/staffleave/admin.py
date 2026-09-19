from django.contrib import admin
from .models import StaffLeave

admin.site.register(StaffLeave)

class StaffLeaveAdmin(admin.ModelAdmin):
    list_display = ('staff', 'from_date', 'to_date', 'leave_type', 'status')
    list_filter = ('leave_type', 'status')
    search_fields = ('staff__first_name', 'staff__last_name', 'reason')

# Register your models here.

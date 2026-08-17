from django.contrib import admin
from apps.customer import models

@admin.register(models.Customer)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code','first_name','last_name','email','mobile_number','gender','date_of_birth','anniversary_date','address','notes','status','created_at','updated_at')

# Register your models here.

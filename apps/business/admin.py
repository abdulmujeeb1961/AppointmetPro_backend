from django.contrib import admin
from .models import Business

from django.contrib import admin
from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        'business_name',
        'owner',
        'business_type',
        'city',
        'status',
        'created_at',
    )

    search_fields = (
        'business_name',
        'owner__username',
        'city',
        'mobile_number',
    )

    list_filter = (
        'business_type',
        'status',
        'city',
    )

    ordering = (
        'business_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )
from django.db import models
from apps.business.models import Business

class HolidayType(models.TextChoices):
    NATIONAL = "NATIONAL" ,"Naional",
    REGIONAL = "REGIONAL", "Regional",
    RELIGIOUS = "RELIGIOUS", "Religious",
    BUSINESS = "BUSINESS" ,"Business",
    OTHER = "OTHER" ,"Other"
    
       

class Holiday(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='holidays')
    holiday_name = models.CharField(max_length=255)
    holiday_date = models.DateField()
    holiday_type = models.CharField(max_length=10, choices=HolidayType.choices, default=HolidayType.BUSINESS)
    is_full_day = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.holiday_name
    
    class meta :
        unique_together = ('business', 'holiday_date')
 
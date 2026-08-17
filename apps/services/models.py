from django.db import models
from apps.business.models import Business

class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'

class Service(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE,related_name="services")
    service_name = models.CharField("Service Name", max_length=100)
    description = models.TextField(blank=True)
    duration_minutes=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    display_order=models.PositiveIntegerField(default=1)
    is_featured=models.BooleanField(default=False)
    is_online_bookable=models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.service_name
    
    class Meta:
        ordering = ['display_order' , 'service_name']
    



from django.db import models
from apps.business.models import Business


class Gender(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    OTHER = 'OTHER', 'Other'
    
class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'

class Customer(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE,related_name="customers")
    customer_code=models.CharField(max_length=20,blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,blank=True)
    email = models.EmailField(null=True,blank=True)
    mobile_number = models.CharField(max_length=10)
    gender=models.CharField(max_length=10,choices=Gender.choices,default=Gender.MALE)
    date_of_birth=models.DateField(null=True,blank=True)
    anniversary_date=models.DateField(null=True,blank=True)
    address=models.TextField(blank=True)
    notes=models.TextField(blank=True)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
     return f"{self.customer_code} - {self.first_name} {self.last_name}"
 
    class Meta:
        ordering=['first_name','last_name'] 
# Create your models here.

from django.db import models
from apps.users.models import User

class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    SUSPENDED = 'SUSPENDED', 'Suspended'
    
    
class BusinessType(models.TextChoices):
    SALON = 'SALON', 'Salon'
    CLINIC = 'CLINIC', 'Clinic'
    HOSPITAL = 'HOSPITAL', 'Hospital'
    SPA = 'SPA', 'Spa'
    GYM = 'GYM', 'Gym'
    COACHING_INSTITUTE = 'COACHING_INSTITUTE', 'Coaching Institute'
    CONSULTANT = 'CONSULTANT', 'Consultant'
    PET_CLINIC = 'PET_CLINIC', 'Pet Clinic'
    OTHER = 'OTHER', 'Other'
    


class Business(models.Model):
    owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='businesses'
)
    business_name = models.CharField('Business Name',max_length=100)
    business_type = models.CharField(max_length=30,choices=BusinessType.choices)
    description = models.TextField(blank=True)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=10)
    address_line_1=models.CharField(max_length=100)
    address_line_2=models.CharField(max_length=100,blank=True)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    pincode=models.CharField(max_length=10)
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.ACTIVE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website=models.URLField(max_length=100,blank=True)
    business_logo=models.ImageField(upload_to='business_logo/',null=True,blank=True)
    currency = models.CharField(
        max_length=3,
        choices=[('INR', 'Indian Rupee'), ('USD', 'US Dollar'), ('EUR', 'Euro')],
        default='INR')
    gst=models.CharField(max_length=20,blank=True)
    pan=models.CharField(max_length=20,blank=True)
    timezone = models.CharField(
    max_length=50,
    default='Asia/Kolkata')
    require_customer_details=models.BooleanField(default=False)
    
    
    
    def __str__(self):
        return f"{self.business_name} - {self.business_type}"
    
    
    class Meta:
        ordering = ['business_name']


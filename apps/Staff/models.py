from django.db import models
from apps.business.models import Business


class Status(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    INACTIVE = 'INACTIVE', 'Inactive'
    
class Gender(models.TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'
    OTHER = 'OTHER', 'Other'
    
class StaffRole(models.TextChoices):
    MANAGER= 'MANAGER', 'Manager'
    STAFF= 'STAFF', 'Staff'
    RECEPTIONIST = "RECEPTIONIST", "Receptionist"
    
class Staff(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE,related_name="staff")
    staff_code=models.CharField(max_length=20,blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True,null=True)
    mobile_number = models.CharField(max_length=10)
    staff_role=models.CharField(max_length=20,choices=StaffRole.choices,default=StaffRole.STAFF)
    designation = models.CharField(max_length=100)
    gender = models.CharField(max_length=10,choices=Gender.choices,default=Gender.MALE)
    joining_date = models.DateField()
    experience_years = models.PositiveIntegerField(default=0)
    profile_photo = models.ImageField(upload_to='staff_profile/',null=True,blank=True)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_bookable=models.BooleanField(default=True)
    notes=models.TextField(blank=True)
    services=models.ManyToManyField('services.Service',blank=True,related_name='staff_members')
    
    def __str__(self):
     return f"{self.staff_code} - {self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']
    
    










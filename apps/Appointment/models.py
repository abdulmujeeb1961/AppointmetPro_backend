from django.db import models
from apps.business.models import Business
from apps.customer.models import Customer
from apps.users.models import User

class BookingSource(models.TextChoices):
  WALK_IN = "WALK_IN", "WALK_IN",
  ONLINE = "ONLINE" , "ONLINE",
  PHONE=  "PHONE" , "PHONE",
  WHATSAPP = "WHATSAPP" , "WHATSAPP"
  
class AppointmentStatus(models.TextChoices):
   BOOKED = "BOOKED", "BOOKED",
   CONFIRMED = "CONFIRMED", "CONFIRMED",
   IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS",
   COMPLETED = "COMPLETED" , "COMPLETED",
   CANCELLED = "CANCELLED" ,"CANCELLED",
   NO_SHOW = "NO_SHOW" , "NO_SHOW"
 

class Appointment(models.Model):
    business =models.ForeignKey(Business, on_delete=models.CASCADE,related_name="appointments")
    appointment_code=models.CharField(max_length=20,blank=True)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE,related_name="appointments")
    appointment_date=models.DateField()
    booking_source=models.CharField(max_length=20,choices=BookingSource.choices,default=BookingSource.WALK_IN)    
    status=models.CharField(max_length=20,choices=AppointmentStatus.choices,default=AppointmentStatus.BOOKED)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="appointments_created",blank=True,null=True)
    notes=models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
     return f"{self.appointment_code} - {self.customer.first_name}"
 
    class Meta:
     ordering = ["-appointment_date", "-created_at"]
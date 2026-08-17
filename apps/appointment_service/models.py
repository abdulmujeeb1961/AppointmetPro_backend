from django.db import models
from apps.Appointment.models import Appointment
from apps.services.models import Service
from apps.Staff.models import Staff
from datetime import datetime  

class AppointmentServiceStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"


class AppointmentService(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,related_name="appointment_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE,related_name="appointment_services")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE,related_name="appointment_services")
    scheduled_start=models.DateTimeField()
    scheduled_end=models.DateTimeField()
    actual_start=models.DateTimeField(null=True,blank=True)
    actual_end=models.DateTimeField(null=True,blank=True)
    status=models.CharField(max_length=20,choices=AppointmentServiceStatus.choices,default=AppointmentServiceStatus.PENDING)
    notes=models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
     return f"{self.appointment.appointment_code} - {self.service.service_name}"
    
    class Meta:
        ordering = ["-scheduled_start"]


# Create your models here.

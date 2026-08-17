from django.db import models


class LeaveType(models.TextChoices):
    FULL_DAY = "FULL_DAY","Full Day",
    PARTIAL_DAY = "PARTIAL_DAY", "Partial Day"
    
class Status(models.TextChoices):
    APPROVED = "APPROVED","Approved",
    CANCELLED = "CANCELLED", "Cancelled"


class StaffLeave(models.Model):
    staff = models.ForeignKey('Staff.Staff', on_delete=models.CASCADE,related_name="staff_leaves")
    leave_date = models.DateField()
    leave_type = models.CharField(max_length=20, choices=LeaveType.choices, default=LeaveType.FULL_DAY)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPROVED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.staff.first_name} {self.staff.last_name}"
    
    class Meta:
        ordering = ['-created_at']
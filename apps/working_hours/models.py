from django.db import models
from apps.Staff.models import Staff


class DayofWeek(models.TextChoices):
    MONDAY = "MONDAY", "Monday"
    TUESDAY = "TUESDAY", "Tuesday"
    WEDNESDAY = "WEDNESDAY", "Wednesday"
    THURSDAY = "THURSDAY", "Thursday"
    FRIDAY = "FRIDAY", "Friday"
    SATURDAY = "SATURDAY", "Saturday"
    SUNDAY = "SUNDAY", "SUNDAY"

class WorkingHours(models.Model):
    staff               = models.ForeignKey('Staff.Staff', on_delete=models.CASCADE,related_name="working_hours")
    day_of_week         = models.CharField(max_length=20,choices=DayofWeek.choices)
    start_time          = models.TimeField()
    end_time            = models.TimeField()
    is_working_day      = models.BooleanField(default=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    
    # Unique constraint is used so that staff is not allotted multiple working hours for the same day. For example, if John is allotted working hours for Monday, then he cannot be allotted working hours for Monday again.
    class Meta:
        ordering = ["staff", "day_of_week"]
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "day_of_week"],
                name="unique_staff_day"
            )
        ]
    
    def __str__(self):
     return f"{self.staff.first_name} - {self.day_of_week}"







from django.db import models
from apps.business.models import Business


class HolidayType(models.TextChoices):
    NATIONAL = "NATIONAL", "National"
    REGIONAL = "REGIONAL", "Regional"
    RELIGIOUS = "RELIGIOUS", "Religious"
    BUSINESS = "BUSINESS", "Business"
    OTHER = "OTHER", "Other"


class Holiday(models.Model):

    business = models.ForeignKey(
        Business,
        on_delete=models.CASCADE,
        related_name="holidays"
    )

    holiday_name = models.CharField(max_length=255)

    holiday_date = models.DateField()

    holiday_type = models.CharField(
        max_length=10,
        choices=HolidayType.choices,
        default=HolidayType.BUSINESS
    )

    notes = models.TextField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.holiday_name


    class Meta:
        unique_together = (
            "business",
            "holiday_date",
        )
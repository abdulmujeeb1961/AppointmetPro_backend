from rest_framework import serializers
from .models import Holiday


class HolidaySerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        business = attrs.get('business')
        holiday_date = attrs.get('holiday_date')

        if business and holiday_date:

            qs = Holiday.objects.filter(
                business=business,
                holiday_date=holiday_date
            )

            # During edit, exclude the current holiday
            if self.instance:
                qs = qs.exclude(
                    pk=self.instance.pk
                )

            # Prevent duplicate holiday for same business and date
            if qs.exists():
                raise serializers.ValidationError(
                    "A holiday on this date already exists for this business."
                )

        return attrs


    class Meta:
        model = Holiday
        fields = '__all__'
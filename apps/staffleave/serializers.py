from rest_framework import serializers
from .models import StaffLeave
from apps.Staff.models import Staff
from apps.working_hours.models import WorkingHours
from apps.holiday.models import Holiday
import calendar


class StaffLeaveSerializer(serializers.ModelSerializer):

    def validate(self, attrs):

        # ---------------------------------------------------------
        # Get values from the incoming request
        # ---------------------------------------------------------

        staff = attrs.get("staff")
        user = self.context["request"].user
        leave_type = attrs.get("leave_type")
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        leave_date = attrs.get("leave_date")

        # ---------------------------------------------------------
        # 1. Check staff ownership
        # ---------------------------------------------------------
        # The logged-in user must be the owner of the business
        # to which this staff member belongs.

        if not Staff.objects.filter(
            business__owner=user,
            pk=staff.pk
        ).exists():

            raise serializers.ValidationError(
                "This staff member does not belong to your business."
            )

        # ---------------------------------------------------------
        # 2. Check whether the date is a business holiday
        # ---------------------------------------------------------
        # At present, we are treating every Holiday record as
        # a FULL-DAY holiday.
        #
        # Therefore, neither FULL_DAY nor PARTIAL_DAY leave
        # should be created on a holiday.

        qs_holiday = Holiday.objects.filter(
            business=staff.business,
            holiday_date=leave_date
        )

        if qs_holiday.exists():

            raise serializers.ValidationError(
                "This date is a holiday for this business. "
                "Staff leave is not required."
            )

        # ---------------------------------------------------------
        # 3. Allow only one leave record for a staff member
        #    on a particular date
        # ---------------------------------------------------------
        #
        # During UPDATE, exclude the current leave record itself.
        # Otherwise, updating an existing leave would incorrectly
        # produce a "leave already exists" error.

        qs = StaffLeave.objects.filter(
            staff=staff,
            leave_date=leave_date
        )

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():

            raise serializers.ValidationError(
                "A leave on this date already exists "
                "for this staff member."
            )

        # ---------------------------------------------------------
        # 4. FULL DAY LEAVE
        # ---------------------------------------------------------
        #
        # A full-day leave must not have start_time or end_time.

        if leave_type == "FULL_DAY":

            if start_time or end_time:

                raise serializers.ValidationError(
                    "Start time and end time cannot be provided "
                    "for full day leaves."
                )

            return attrs

        # ---------------------------------------------------------
        # 5. Find the staff member's working day
        # ---------------------------------------------------------
        #
        # Example:
        # leave_date = Thursday
        #       ↓
        # "THURSDAY"
        #       ↓
        # Find Thursday's WorkingHours for this staff member.

        leave_day = (
            calendar.day_name[leave_date.weekday()]
        ).upper()

        weekday = WorkingHours.objects.filter(
            staff=staff,
            day_of_week=leave_day
        ).first()

        # No WorkingHours record found for this day.

        if weekday is None:

            raise serializers.ValidationError(
                "This staff member is not working on this day."
            )

        # WorkingHours record exists, but staff is marked
        # as not working on this day.

        if not weekday.is_working_day:

            raise serializers.ValidationError(
                "This staff member is not working on this day."
            )

        # ---------------------------------------------------------
        # 6. PARTIAL DAY LEAVE
        # ---------------------------------------------------------

        if leave_type == "PARTIAL_DAY":

            # Both start and end times are mandatory.

            if start_time is None or end_time is None:

                raise serializers.ValidationError(
                    "Start time and end time must be provided."
                )

            # Start time must be earlier than end time.

            if start_time >= end_time:

                raise serializers.ValidationError(
                    "Start time must be earlier than end time."
                )

            # Leave must fall completely within the staff member's
            # working hours.

            if (
                start_time < weekday.start_time
                or end_time > weekday.end_time
            ):

                raise serializers.ValidationError(
                    "Start time and end time must be "
                    "within working hours."
                )

            return attrs

        # ---------------------------------------------------------
        # If we reach here, return the validated data.
        # ---------------------------------------------------------

        return attrs

    class Meta:
        model = StaffLeave
        fields = "__all__"
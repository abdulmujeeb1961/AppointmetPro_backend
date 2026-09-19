from rest_framework import serializers
from .models import StaffLeave

from apps.Staff.models import Staff
from apps.working_hours.models import WorkingHours
from apps.holiday.models import Holiday

import calendar


class StaffLeaveSerializer(serializers.ModelSerializer):
    staff_name=serializers.SerializerMethodField()

    def get_staff_name(self, obj):
        return f"{obj.staff.first_name} {obj.staff.last_name}".strip()

    def validate(self, attrs):

        # =========================================================
        # GET DATA FROM THE REQUEST
        # =========================================================

        staff = attrs.get("staff")

        from_date = attrs.get("from_date")
        to_date = attrs.get("to_date")

        leave_type = attrs.get("leave_type")

        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        user = self.context["request"].user


        # =========================================================
        # 1. CHECK STAFF OWNERSHIP
        # =========================================================
        #
        # We must ensure that the selected staff belongs to a
        # business owned by the logged-in user.
        #
        # Example:
        #
        # Logged-in user
        #       ↓
        # Business Owner
        #       ↓
        # Business
        #       ↓
        # Staff
        #

        if not Staff.objects.filter(
            business__owner=user,
            pk=staff.pk
        ).exists():

            raise serializers.ValidationError(
                "This staff member does not belong to your business."
            )


        # =========================================================
        # 2. CHECK THAT FROM DATE IS NOT GREATER THAN TO DATE
        # =========================================================
        #
        # Example of INVALID leave:
        #
        # From Date = 20 September
        # To Date   = 10 September
        #

        if from_date > to_date:

            raise serializers.ValidationError(
                "From date cannot be later than to date."
            )


        # =========================================================
        # 3. CHECK FOR OVERLAPPING LEAVES
        # =========================================================
        #
        # We need to check whether this staff member already has
        # another leave during any part of the selected date range.
        #
        # Example:
        #
        # Existing Leave:
        # 10 September → 15 September
        #
        # New Leave:
        # 12 September → 20 September
        #
        # These overlap.
        #
        #
        # The logic is:
        #
        # Existing From Date <= New To Date
        #
        # AND
        #
        # Existing To Date >= New From Date
        #

        overlapping_leaves = StaffLeave.objects.filter(

            # Same staff member
            staff=staff,

            # Existing leave starts before or on
            # the new leave ending date
            from_date__lte=to_date,

            # Existing leave ends after or on
            # the new leave starting date
            to_date__gte=from_date,

        ).exclude(

            # Cancelled leaves should not block
            # a new leave application
            status="CANCELLED"

        )


        # =========================================================
        # 4. DURING EDIT, EXCLUDE THE CURRENT LEAVE RECORD
        # =========================================================
        #
        # Suppose Leave ID 5 is:
        #
        # 10 September → 15 September
        #
        # When we edit Leave ID 5, the overlap query will find
        # Leave ID 5 itself.
        #
        # Therefore, we must exclude the current record.
        #

        if self.instance:

            overlapping_leaves = overlapping_leaves.exclude(
                pk=self.instance.pk
            )


        # =========================================================
        # 5. IF ANY OVERLAPPING LEAVE EXISTS, STOP
        # =========================================================

        if overlapping_leaves.exists():

            raise serializers.ValidationError(
                "The selected leave dates overlap with an existing leave."
            )


        # =========================================================
        # 6. CHECK BUSINESS HOLIDAYS
        # =========================================================
        #
        # We check whether any holiday exists between:
        #
        # from_date → to_date
        #
        # Example:
        #
        # Leave:
        # 10 September → 15 September
        #
        # Holiday:
        # 12 September
        #
        # A holiday exists within the leave period.
        #
        # For the moment, we will prevent the leave from covering
        # a business holiday.
        #

        holidays = Holiday.objects.filter(

            business=staff.business,

            holiday_date__gte=from_date,

            holiday_date__lte=to_date,

        )


        if holidays.exists():

            raise serializers.ValidationError(
                "The selected leave period includes a business holiday."
            )


        # =========================================================
        # 7. MULTI-DAY LEAVE MUST BE FULL DAY
        # =========================================================
        #
        # Example:
        #
        # From Date = 10 September
        # To Date   = 15 September
        #
        # This is more than one day.
        #
        # Therefore, PARTIAL_DAY leave should not be allowed.
        #

        if from_date != to_date:

            if leave_type != "FULL_DAY":

                raise serializers.ValidationError(
                    "Partial day leave can only be applied for a single day."
                )


        # =========================================================
        # 8. FULL DAY LEAVE VALIDATION
        # =========================================================
        #
        # Full-day leave should not contain start_time or end_time.
        #
        # Example:
        #
        # FULL_DAY
        #
        # Start Time = empty
        # End Time   = empty
        #

        if leave_type == "FULL_DAY":

            if start_time or end_time:

                raise serializers.ValidationError(
                    "Start time and end time cannot be provided "
                    "for full day leave."
                )

            # All validation for FULL_DAY leave is complete.

            return attrs


        # =========================================================
        # 9. PARTIAL DAY LEAVE VALIDATION
        # =========================================================
        #
        # Partial leave can only be for ONE date.
        #
        # Therefore:
        #
        # from_date must equal to_date
        #

        if leave_type == "PARTIAL_DAY":

            if from_date != to_date:

                raise serializers.ValidationError(
                    "Partial day leave can only be applied for one day."
                )


            # =====================================================
            # 10. BOTH START AND END TIMES ARE REQUIRED
            # =====================================================

            if start_time is None or end_time is None:

                raise serializers.ValidationError(
                    "Start time and end time must be provided "
                    "for partial day leave."
                )


            # =====================================================
            # 11. START TIME MUST BE BEFORE END TIME
            # =====================================================

            if start_time >= end_time:

                raise serializers.ValidationError(
                    "Start time must be earlier than end time."
                )


            # =====================================================
            # 12. FIND THE DAY OF THE WEEK
            # =====================================================
            #
            # Example:
            #
            # from_date = 2026-09-14
            #
            # Python finds:
            #
            # MONDAY
            #

            leave_day = calendar.day_name[
                from_date.weekday()
            ].upper()


            # =====================================================
            # 13. GET WORKING HOURS FOR THAT DAY
            # =====================================================
            #
            # Find the staff member's WorkingHours record.
            #
            # Example:
            #
            # Staff = John
            # Day   = MONDAY
            #

            working_hours = WorkingHours.objects.filter(

                staff=staff,

                day_of_week=leave_day

            ).first()


            # =====================================================
            # 14. CHECK WHETHER WORKING HOURS EXIST
            # =====================================================

            if working_hours is None:

                raise serializers.ValidationError(
                    "Working hours are not available for this staff member "
                    "on the selected day."
                )


            # =====================================================
            # 15. CHECK WHETHER STAFF WORKS ON THAT DAY
            # =====================================================
            #
            # Example:
            #
            # Monday:
            #
            # is_working_day = False
            #
            # Then the staff member cannot apply for leave because
            # the staff member is already not scheduled to work.
            #

            if not working_hours.is_working_day:

                raise serializers.ValidationError(
                    "This staff member is not working on the selected day."
                )


            # =====================================================
            # 16. CHECK THAT LEAVE TIME IS WITHIN WORKING HOURS
            # =====================================================
            #
            # Example:
            #
            # Working Hours:
            #
            # 09:00 → 17:00
            #
            # Valid Partial Leave:
            #
            # 10:00 → 13:00
            #
            #
            # Invalid Partial Leave:
            #
            # 08:00 → 12:00
            #

            if start_time < working_hours.start_time:

                raise serializers.ValidationError(
                    "Leave start time cannot be earlier than "
                    "the staff member's working hours."
                )


            if end_time > working_hours.end_time:

                raise serializers.ValidationError(
                    "Leave end time cannot be later than "
                    "the staff member's working hours."
                )


            # All PARTIAL_DAY validation is complete.

            return attrs


        # =========================================================
        # RETURN VALIDATED DATA
        # =========================================================

        return attrs


    class Meta:
        model = StaffLeave
        fields = [
            "id",
            "staff",
            "staff_name",
            "from_date",
            "to_date",
            "leave_type",
            "reason",
            "status",
        ]
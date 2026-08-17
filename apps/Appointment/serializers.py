from rest_framework import serializers
from apps.Appointment.models import Appointment
from apps.services.models import Service
from apps.Staff.models import Staff
from apps.holiday.models import Holiday
from apps.working_hours.models import WorkingHours
from apps.staffleave.models import StaffLeave
from apps.appointment_service.models import AppointmentService
from datetime import date
import calendar
from datetime import datetime, timedelta
from django.db.models import Q
from django.db import transaction
from apps.Appointment.models import BookingSource


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]

    def validate_appointment_date(self, value):

        if value < date.today():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    def validate_notes(self, value):
        if value:
            value = value.strip()
        return value

    def validate(self, attrs):
        business = attrs.get("business")
        customer = attrs.get("customer")

        if customer.business != business:
            raise serializers.ValidationError(
                {"customer": "Customer does not belong to this business."}
            )

        if business.owner != self.context["request"].user:
            raise serializers.ValidationError(
                {"business": "You are not authorized to manage this business."}
            )

        return attrs





class BookingSerializer(serializers.Serializer):

    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all()
    )

    appointment_date = serializers.DateField()

    start_time = serializers.TimeField()

    staff = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(),
        required=False
    )

    first_name = serializers.CharField(
        max_length=100,
        required=False
    )

    last_name = serializers.CharField(
        max_length=100,
        required=False
    )

    mobile_number = serializers.CharField(
        max_length=10,
        required=False
    )

    email = serializers.EmailField(
        required=False
    )

    def validate(self, attrs):

        # ---------------------------------------------------------
        # 1. Get the values supplied by the customer
        # ---------------------------------------------------------

        service = attrs.get("service")
        staff = attrs.get("staff")
        appointment_date = attrs.get("appointment_date")
        start_time = attrs.get("start_time")

        # ---------------------------------------------------------
        # 2. Basic service validation
        # ---------------------------------------------------------

        if not service.is_online_bookable:
            raise serializers.ValidationError(
                "This service is not online bookable."
            )

        if service.status == "INACTIVE":
            raise serializers.ValidationError(
                "This service is not active."
            )

        # The business is obtained from the selected service.
        business = service.business

        # Check whether this business requires customer details.
        require_customer_details = business.require_customer_details

        # ---------------------------------------------------------
        # 3. Customer details validation
        # ---------------------------------------------------------

        if require_customer_details:

            first_name = attrs.get("first_name")
            mobile_number = attrs.get("mobile_number")

            # For businesses such as clinics/dentists, these are mandatory.
            if not first_name or not mobile_number:
                raise serializers.ValidationError(
                    "First Name and Mobile number details are required."
                )

        # ---------------------------------------------------------
        # 4. Appointment date validation
        # ---------------------------------------------------------

        # Appointment date cannot be in the past.
        if appointment_date < date.today():
            raise serializers.ValidationError(
                "Appointment date cannot be in the past."
            )

        # Determine the day of the week.
        appointment_day = calendar.day_name[
            appointment_date.weekday()
        ].upper()

        # ---------------------------------------------------------
        # 5. Business holiday check
        # ---------------------------------------------------------

        if Holiday.objects.filter(
            business=business,
            holiday_date=appointment_date
        ).exists():

            raise serializers.ValidationError(
                "This date is a holiday."
            )

        # ---------------------------------------------------------
        # 6. Calculate appointment end time
        # ---------------------------------------------------------

        # We know:
        # start_time + service duration = end_time

        end_datetime = (
            datetime.combine(appointment_date, start_time)
            + timedelta(minutes=service.duration_minutes)
        )

        end_time = end_datetime.time()

        # These datetime values are required for the
        # double-booking/overlap check.
        new_start = datetime.combine(
            appointment_date,
            start_time
        )

        new_end = datetime.combine(
            appointment_date,
            end_time
        )

        # ---------------------------------------------------------
        # 7. CUSTOMER HAS SPECIFICALLY REQUESTED A STAFF MEMBER
        # ---------------------------------------------------------

        if staff:

            # Staff must belong to the same business as the service.
            if staff.business != business:
                raise serializers.ValidationError(
                    "This staff member does not belong to this business."
                )

            # Staff must be assigned to provide this service.
            if not staff.services.filter(
                pk=service.pk
            ).exists():

                raise serializers.ValidationError(
                    "This staff member is not assigned to provide this service."
                )

            # Staff must be active and bookable.
            if staff.status != "ACTIVE":
                raise serializers.ValidationError(
                    "This staff member is not active."
                )

            if not staff.is_bookable:
                raise serializers.ValidationError(
                    "This staff member is not available for booking."
                )

            # -----------------------------------------------------
            # 8. Check staff working day
            # -----------------------------------------------------

            weekday = WorkingHours.objects.filter(
                staff=staff,
                day_of_week=appointment_day
            ).first()

            if weekday is None or not weekday.is_working_day:
                raise serializers.ValidationError(
                    "This staff member is not working on this day."
                )

            # -----------------------------------------------------
            # 9. Check staff working hours
            # -----------------------------------------------------

            if (
                start_time < weekday.start_time
                or end_time > weekday.end_time
            ):

                raise serializers.ValidationError(
                    "This staff member is not working during this time."
                )

            # -----------------------------------------------------
            # 10. Check staff leave
            # -----------------------------------------------------

            staffleave = StaffLeave.objects.filter(
                staff=staff,
                leave_date=appointment_date
            ).first()

            if staffleave:

                # Full-day leave means the entire day is unavailable.
                if staffleave.leave_type == "FULL_DAY":

                    raise serializers.ValidationError(
                        "This staff member is on leave on this day."
                    )

                # Partial-day leave means we must check
                # whether the requested appointment overlaps the leave.
                if staffleave.leave_type == "PARTIAL_DAY":

                    if (
                        start_time < staffleave.end_time
                        and end_time > staffleave.start_time
                    ):

                        raise serializers.ValidationError(
                            "This staff member is on leave during this time."
                        )

            # -----------------------------------------------------
            # 11. Check double booking
            # -----------------------------------------------------

            # Find whether this staff member already has
            # ANY appointment overlapping the requested time.

            staff_appointment = (
                AppointmentService.objects.filter(
                    staff=staff,
                    appointment__appointment_date=appointment_date,
                    scheduled_start__lt=new_end,
                    scheduled_end__gt=new_start,
                )
                .exclude(status="CANCELLED")
                .exists()
            )

            if staff_appointment:

                raise serializers.ValidationError(
                    "This staff member has an appointment during this time."
                )

        # ---------------------------------------------------------
        # 12. CUSTOMER HAS NOT REQUESTED A SPECIFIC STAFF MEMBER
        # ---------------------------------------------------------

        else:

            # Find active and bookable staff who can provide
            # the requested service.
            candidate_staff = Staff.objects.filter(
                status="ACTIVE",
                is_bookable=True,
                services=service,
                business=business,
            ).distinct()

            available_staff = None

            # Check each candidate one by one.
            for staff_member in candidate_staff:

                # -------------------------------------------------
                # Check working day
                # -------------------------------------------------

                weekday = WorkingHours.objects.filter(
                    staff=staff_member,
                    day_of_week=appointment_day
                ).first()

                if weekday is None or not weekday.is_working_day:
                    continue

                # -------------------------------------------------
                # Check working hours
                # -------------------------------------------------

                if (
                    start_time < weekday.start_time
                    or end_time > weekday.end_time
                ):
                    continue

                # -------------------------------------------------
                # Check staff leave
                # -------------------------------------------------

                staffleave = StaffLeave.objects.filter(
                    staff=staff_member,
                    leave_date=appointment_date
                ).first()

                if staffleave:

                    # Full-day leave
                    if staffleave.leave_type == "FULL_DAY":
                        continue

                    # Partial-day leave
                    if staffleave.leave_type == "PARTIAL_DAY":

                        if (
                            start_time < staffleave.end_time
                            and end_time > staffleave.start_time
                        ):
                            continue

                # -------------------------------------------------
                # Check double booking
                # -------------------------------------------------

                staff_appointment = (
                    AppointmentService.objects.filter(
                        staff=staff_member,
                        appointment__appointment_date=appointment_date,
                        scheduled_start__lt=new_end,
                        scheduled_end__gt=new_start,
                    )
                    .exclude(status="CANCELLED")
                    .exists()
                )

                # If this staff member already has an overlapping
                # appointment, move to the next staff member.
                if staff_appointment:
                    continue

                # -------------------------------------------------
                # This staff member is available
                # -------------------------------------------------

                available_staff = staff_member
                break

            # -----------------------------------------------------
            # 13. No staff member was available
            # -----------------------------------------------------

            if available_staff is None:

                raise serializers.ValidationError(
                    "No staff member is available for the selected time."
                )

            # Save the automatically selected staff member
            # into attrs so that the create() method can use it.
            attrs["staff"] = available_staff

        # Return validated data.
        return attrs
    

        @transaction.atomic
        def create(self, validated_data):
            service=validated_data.get("service")
            staff=validated_data.get("staff")
            appointment_date=validated_data.get("appointment_date")
            start_time=validated_data.get("start_time")
            first_name=validated_data.get("first_name")
            last_name=validated_data.get("last_name")   
            mobile_number=validated_data.get("mobile_number")
            email=validated_data.get("email")
            business=service.business
            end_datetime = (datetime.combine(appointment_date, start_time)
            + timedelta(minutes=service.duration_minutes))

            end_time = end_datetime.time()
           
            
            customer=Customer.objects.filter(business=business,mobile_number=mobile_number).first()
            
            if not customer:
                customer=Customer.objects.create(business=business,first_name=first_name,mobile_number=mobile_number,last_name=last_name,email=email)
            
            appointment=Appointment.objects.create(business=business,customer=customer,appointment_date=appointment_date,booking_source=BookingSource.ONLINE,created_by=None)
            
            appointment_service=AppointmentService.objects.create(appointment=appointment,service=service,staff=staff,scheduled_start=datetime.combine(appointment_date,start_time),scheduled_end=datetime.combine(appointment_date,end_time))
            return appointment
            
            
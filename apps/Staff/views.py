from django.shortcuts import render
from .models import Staff
from apps.business.models import Business
from .serializers import StaffSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from apps.working_hours.models import WorkingHours, DayofWeek


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Staff.objects.filter(business__owner=self.request.user) # Here also Staff model does not have owner field which is a part of Business model. So in order to access it we use business model and the way to access it business__owner

    def perform_create(self, serializer):
        # Get the selected business from the validated serializer data
        business = serializer.validated_data["business"]

        # Ensure the logged-in user owns the selected business
        if business.owner != self.request.user:
            raise PermissionDenied(
                "You are not allowed to add staff to this business."
            )

        # Find the latest staff member for this business
        last_staff = Staff.objects.filter(
            business=business
        ).order_by("-id").first() # -id is used to sort in descending order. if there are EMP1,EMP2,EMP3 then first .first() will return EMP3

        # Generate the next staff code. If the staff code is generated for the first time, it will be EMP001
        if not last_staff:
            staff_code = "EMP001"
        else:
            last_number = int(last_staff.staff_code[3:]) # [3:] means start from index 3. EMP003 willreturn 003 and int will return 3
            staff_code = f"EMP{last_number + 1:03d}" # :03 means keep 3 digits i.e 003,099,100 and so on.  So last number will become EMP004 if the previous code was EMP003
            
       
            
        

        # Save the new staff member with the generated staff code
        new_staff= serializer.save(staff_code=staff_code)
        
        days = [choice.value for choice in DayofWeek]

        for day in days:
            WorkingHours.objects.create(
                staff=new_staff,
                day_of_week=day,
                start_time="09:00",
                end_time="17:00",
                is_working_day=True
            )
from apps.staffleave.models import StaffLeave
from rest_framework import viewsets
from .serializers import StaffLeaveSerializer
from rest_framework.permissions import IsAuthenticated


class StaffLeaveViewSet(viewsets.ModelViewSet):

    queryset = StaffLeave.objects.all()
    serializer_class = StaffLeaveSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        # Get logged-in user
        user = self.request.user


        # ==========================================
        # STEP 1: Decide which records the user
        # is allowed to see
        # ==========================================

        if user.role == 'SUPER_ADMIN':

            queryset = StaffLeave.objects.all()


        elif user.role == 'BUSINESS_OWNER':

            queryset = StaffLeave.objects.filter(
                staff__business__owner=user
            )


        elif user.role == 'STAFF':

            # Check whether the User has a Staff profile
            if not hasattr(user, 'staff_profile'):

                queryset = StaffLeave.objects.none()

            else:

                staff_profile = user.staff_profile


                # Manager and Receptionist can see
                # leaves of all staff in their business

                if staff_profile.staff_role in [
                    'MANAGER',
                    'RECEPTIONIST'
                ]:

                    queryset = StaffLeave.objects.filter(
                        staff__business=staff_profile.business
                    )

                else:

                    # Normal staff cannot see all leave records
                    queryset = StaffLeave.objects.none()


        else:

            queryset = StaffLeave.objects.none()


        # ==========================================
        # STEP 2: Filter by Staff ID if provided
        # ==========================================

        staff_id = self.request.query_params.get('staff')

        if staff_id:

            queryset = queryset.filter(
                staff_id=staff_id
            )


        return queryset
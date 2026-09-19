from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import HolidaySerializer
from .models import Holiday


class HolidayViewSet(viewsets.ModelViewSet):

    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):

        user = self.request.user


        # ==========================================
        # SUPER ADMIN
        # Can see holidays of all businesses
        # ==========================================

        if user.role == 'SUPER_ADMIN':

            return Holiday.objects.all()


        # ==========================================
        # BUSINESS OWNER
        # Can see holidays of all businesses
        # owned by this user
        # ==========================================

        elif user.role == 'BUSINESS_OWNER':

            return Holiday.objects.filter(
                business__owner=user
            )


        # ==========================================
        # STAFF USER
        # Check Manager / Receptionist
        # ==========================================

        elif user.role == 'STAFF':

            if hasattr(user, 'staff_profile'):

                staff_profile = user.staff_profile


                # MANAGER / RECEPTIONIST
                # Can see holidays of their own business

                if staff_profile.staff_role in [
                    'MANAGER',
                    'RECEPTIONIST'
                ]:

                    return Holiday.objects.filter(
                        business=staff_profile.business
                    )


            # Ordinary Staff
            # Currently no access

            return Holiday.objects.none()


        # ==========================================
        # Any other role
        # ==========================================

        return Holiday.objects.none()
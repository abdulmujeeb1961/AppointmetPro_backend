from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import HolidaySerializer
from .models import Holiday



class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
       
        return Holiday.objects.filter(business__owner=user)

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import WorkingHoursSerializer
from .models import WorkingHours

class WorkingHoursViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer
    
    
    def get_queryset(self):
        return WorkingHours.objects.filter(staff__business__owner=self.request.user)

# Create your views here.

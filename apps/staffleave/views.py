from django.shortcuts import render
from apps.staffleave.models import StaffLeave
from rest_framework import viewsets
from .serializers import StaffLeaveSerializer
from rest_framework.permissions import IsAuthenticated


class StaffLeaveViewSet(viewsets.ModelViewSet):
    queryset = StaffLeave.objects.all()
    serializer_class = StaffLeaveSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user=self.request.user
        return StaffLeave.objects.filter(staff__business__owner=user)

# Create your views here.

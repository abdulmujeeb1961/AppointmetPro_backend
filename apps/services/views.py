from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ServiceSerializer
from .models import Service
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class ServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    # This method is used to filter the business and services based on the logged in user.  For example the logged in user has two businesses, Gym and Salon.  If he logs in to the Gym business, he will only see the services of the Gym business.  In the service table there is no owner field, it is in Business table. So to access the owner we have to write business__owner.
    def get_queryset(self):
        return Service.objects.filter(business__owner=self.request.user).order_by("business__business_name","service_name")
            
       
        
# =============================================================================
# perform_create() - Why do we override it?
# =============================================================================
#
# DRF's ModelViewSet already provides a built-in create() method.
#
# Internally it performs the following steps:
#
#   1. serializer = ServiceSerializer(data=request.data)
#   2. serializer.is_valid()
#   3. perform_create(serializer)
#   4. serializer.save()
#   5. return Response(...)
#
# We override perform_create() when we need to execute some custom logic
# BEFORE saving the object.
#
# -----------------------------------------------------------------------------
# Example
# -----------------------------------------------------------------------------
#
# Suppose two users exist:
#
#   Abdul
#   John
#
# Business table
#
#   ID   Business Name      Owner
#   --------------------------------
#   1    ABC Salon          Abdul
#   2    ABC Gym            Abdul
#   3    John's Clinic      John
#
# Abdul logs in and wants to create a new service "Hair Cut" for his salon.
#
# Frontend sends:
#
# {
#     "business": 1,
#     "service_name": "Hair Cut",
#     "duration_minutes": 30,
#     "price": 300
# }
#
# During serializer.is_valid(), DRF automatically converts the business ID
# into the actual Business object.
#
# serializer.validated_data becomes:
#
# {
#     "business": <Business: ABC Salon>,
#     "service_name": "Hair Cut",
#     "duration_minutes": 30,
#     "price": Decimal("300.00"),
#     ...
# }
#
# Therefore, inside perform_create() we can directly access:
#
#     business = serializer.validated_data["business"]
#
# Notice that 'business' is now a Business model object, NOT the integer 1.
#
# -----------------------------------------------------------------------------
# Why do we check ownership?
# -----------------------------------------------------------------------------
#
# A malicious user could bypass the frontend and send:
#
# {
#     "business": 3
# }
#
# where Business 3 belongs to John.
#
# Therefore, before saving, the backend MUST verify:
#
#     Does the selected Business belong to the logged-in user?
#
# If
#
#     business.owner == self.request.user
#
# then
#
#     serializer.save()
#
# else
#
#     raise PermissionDenied(
#         "You are not allowed to add services to this business."
#     )
#
# This prevents one owner from creating services for another owner's business.
#
# =============================================================================

# =============================================================================
# perform_create() - Why do we override it?
# =============================================================================
#
# DRF's ModelViewSet already provides a built-in create() method.
#
# Internally it performs the following steps:
#
#   1. serializer = ServiceSerializer(data=request.data)
#   2. serializer.is_valid()
#   3. perform_create(serializer)
#   4. serializer.save()
#   5. return Response(...)
#
# We override perform_create() when we need to execute some custom logic
# BEFORE saving the object.
#
# -----------------------------------------------------------------------------
# Example
# -----------------------------------------------------------------------------
#
# Suppose two users exist:
#
#   Abdul
#   John
#
# Business table
#
#   ID   Business Name      Owner
#   --------------------------------
#   1    ABC Salon          Abdul
#   2    ABC Gym            Abdul
#   3    John's Clinic      John
#
# Abdul logs in and wants to create a new service "Hair Cut" for his salon.
#
# Frontend sends:
#
# {
#     "business": 1,
#     "service_name": "Hair Cut",
#     "duration_minutes": 30,
#     "price": 300
# }
#
# During serializer.is_valid(), DRF automatically converts the business ID
# into the actual Business object.
#
# serializer.validated_data becomes:
#
# {
#     "business": <Business: ABC Salon>,
#     "service_name": "Hair Cut",
#     "duration_minutes": 30,
#     "price": Decimal("300.00"),
#     ...
# }
#
# Therefore, inside perform_create() we can directly access:
#
#     business = serializer.validated_data["business"]
#
# Notice that 'business' is now a Business model object, NOT the integer 1.
#
# -----------------------------------------------------------------------------
# Why do we check ownership?
# -----------------------------------------------------------------------------
#
# A malicious user could bypass the frontend and send:
#
# {
#     "business": 3
# }
#
# where Business 3 belongs to John.
#
# Therefore, before saving, the backend MUST verify:
#
#     Does the selected Business belong to the logged-in user?
#
# If
#
#     business.owner == self.request.user
#
# then
#
#     serializer.save()
#
# else
#
#     raise PermissionDenied(
#         "You are not allowed to add services to this business."
#     )
#
# This prevents one owner from creating services for another owner's business.
#
# =============================================================================
    

def perform_create(self, serializer):
    # Get the Business object selected by the frontend
    business = serializer.validated_data["business"]

    # Check whether this business belongs to the logged-in user
    if business.owner != self.request.user:
        raise PermissionDenied(
            "You are not allowed to add services to this business."
        )

    # Save the service
    serializer.save()
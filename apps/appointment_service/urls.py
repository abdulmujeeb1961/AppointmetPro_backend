from apps.appointment_service.views import AppointmentServiceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'appointmentservices', AppointmentServiceViewSet, basename='appointmentservices')

urlpatterns = router.urls

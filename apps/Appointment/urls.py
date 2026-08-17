from apps.Appointment.views import AppointmentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet, basename="appointments")

urlpatterns = router.urls
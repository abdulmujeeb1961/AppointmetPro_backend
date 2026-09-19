from apps.Appointment.views import AppointmentViewSet,BookingViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet, basename="appointments")
router.register(r"bookings", BookingViewSet, basename="bookings")

urlpatterns = router.urls
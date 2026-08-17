from apps.holiday.views import HolidayViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('holiday', HolidayViewSet, basename='holiday')

urlpatterns = router.urls
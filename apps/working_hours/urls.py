from apps.working_hours.views import WorkingHoursViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'working_hours', WorkingHoursViewSet, basename='working_hours')
router

urlpatterns = router.urls
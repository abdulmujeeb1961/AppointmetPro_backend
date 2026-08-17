from apps.Staff.views import StaffViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'staff', StaffViewSet, basename='staff')

urlpatterns = router.urls
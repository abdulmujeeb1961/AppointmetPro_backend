from apps.staffleave.views import StaffLeaveViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'staffleave', StaffLeaveViewSet, basename='staffleave')

urlpatterns = router.urls
from apps.services.views import ServiceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='services')

urlpatterns = router.urls
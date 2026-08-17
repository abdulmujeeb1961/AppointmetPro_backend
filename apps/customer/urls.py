from apps.customer.views import CustomerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers',CustomerViewSet,basename='customer')

urlpatterns = router.urls
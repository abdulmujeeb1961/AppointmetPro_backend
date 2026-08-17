from apps.business.views import BusinessViewSet, BusinessListViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'businesses', BusinessViewSet, basename='business')
router.register(r'businesslist', BusinessListViewSet, basename='businesslist')


urlpatterns = router.urls
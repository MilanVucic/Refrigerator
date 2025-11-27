from rest_framework.routers import DefaultRouter
from .views import FridgeViewSet

router = DefaultRouter()
router.register(r'fridges', FridgeViewSet, basename='fridge')

urlpatterns = router.urls

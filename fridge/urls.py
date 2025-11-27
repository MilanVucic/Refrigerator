from rest_framework.routers import DefaultRouter
from .views import FridgeViewSet, ItemViewSet

router = DefaultRouter()
router.register(r'fridges', FridgeViewSet, basename='fridge')
router.register(r'items', ItemViewSet, basename='item')

urlpatterns = router.urls

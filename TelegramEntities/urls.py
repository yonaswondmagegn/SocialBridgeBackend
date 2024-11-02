from rest_framework_nested import routers
from .views import LoadenedEntitiyViewSet

router = routers.DefaultRouter()
router.register('history', LoadenedEntitiyViewSet, basename='loadened-entities')

urlpatterns = router.urls


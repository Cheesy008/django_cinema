from rest_framework.routers import DefaultRouter

from .views import MovieViewSet

app_name = 'api'

router = DefaultRouter()
router.register('movie', MovieViewSet, basename='movie')

urlpatterns = router.urls

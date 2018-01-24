from rest_framework.routers import DefaultRouter

from api.views import AccountViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='account')
urlpatterns = router.urls

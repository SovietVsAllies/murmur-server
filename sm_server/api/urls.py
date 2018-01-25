from rest_framework.routers import DefaultRouter

from api.views import AccountViewSet, PreKeyViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='account')
router.register(r'pre_keys', PreKeyViewSet, base_name='pre_key')
urlpatterns = router.urls

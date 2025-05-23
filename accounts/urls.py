from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from .views import InvitationViewSet, RequestViewSet, UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("invitations", InvitationViewSet, basename="invitations")
router.register("requests", RequestViewSet, basename="requests")
router.register("", UserViewSet, basename="users")

urlpatterns = router.urls

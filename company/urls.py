from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, InvitationViewSet, RequestViewSet

router = DefaultRouter(trailing_slash=False)
router.register("invitations", InvitationViewSet, basename="invitations")
router.register("requests", RequestViewSet, basename="requests")
router.register("", CompanyViewSet, basename="companies")

urlpatterns = router.urls

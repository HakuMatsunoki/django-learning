from django.urls import path

from .views import CheckHealthView

urlpatterns = [path("", CheckHealthView.as_view(), name="check_health")]

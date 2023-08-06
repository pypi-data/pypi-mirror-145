from django.conf.urls import include
from django.urls import path
from rest_framework.routers import SimpleRouter

from ob_dj_otp.apis.otp.views import OneTimePairingViewSet

app_name = "otp"

router = SimpleRouter(trailing_slash=False)

router.register(r"", OneTimePairingViewSet, basename="otp"),

urlpatterns = [
    path("", include(router.urls)),
]

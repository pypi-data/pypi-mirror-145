from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("otp/", include("ob_dj_otp.apis.otp.urls", namespace="otp")),
]

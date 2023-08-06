from django.core.exceptions import PermissionDenied
from django.urls import resolve
from django.utils.translation import gettext_lazy as _


class OTPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        resolver_match = resolve(request.path)
        if resolver_match.url_name == "auth:login":
            raise PermissionDenied(
                _("You only get the authentication token through OTP")
            )

        response = self.get_response(request)
        return response

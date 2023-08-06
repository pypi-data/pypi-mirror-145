import string
import typing
from random import sample

from django.conf import settings
from django.db import models


class OneTruePairingManager(models.Manager):
    def create(self, *args: typing.Any, **kwargs: typing.Any):
        if "verification_code" not in kwargs:
            verification_code = None
            # If OTP_FORCE_CODE is set, hard code the value
            if getattr(settings, "OTP_FORCE_CODE", False):
                verification_code = settings.OTP_FORCE_CODE
            # If OTP_FORCE_CODE not set, generate a 5 digit number
            # and store as string
            if not verification_code:
                code_length = getattr(settings, "OTP_CODE_LENGTH", 5)
                verification_code = "".join(sample(string.digits, code_length))

            kwargs["verification_code"] = verification_code
        return super().create(*args, **kwargs)

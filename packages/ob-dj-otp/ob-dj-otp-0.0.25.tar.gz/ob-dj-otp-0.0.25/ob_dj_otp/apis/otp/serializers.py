import logging
import typing
from datetime import timedelta
from functools import reduce
from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from ob_dj_otp.core.otp.models import OneTruePairing

logger = logging.getLogger(__name__)


class OTPSerialzerMixin:
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if getattr(settings, "OTP_PHONE_NUMBER_AS_PRIMARY_FIELD", False):
            # extra_kwargs don't affect phine_number params :/
            self.fields["phone_number"].required = True

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if getattr(settings, "OTP_EMAIL_AS_PRIMARY_FIELD", False):
            extra_kwargs.setdefault("email", {}).update(required=True)

        return extra_kwargs

    def validate(self, attrs: typing.Dict) -> typing.Dict:
        if not (attrs.get("email") or attrs.get("phone_number")):
            raise ValidationError(_("Email or Phone number is required."))
        self.otp_kwargs = {
            k: v for k, v in attrs.items() if k in ["email", "phone_number"] and v
        }
        self.otp_sub_message = " or ".join(self.otp_kwargs.keys())
        self.otp_query = reduce(
            lambda x, y: x | y, [Q(**{k: v}) for k, v in self.otp_kwargs.items()]
        )
        return super().validate(attrs)


class OTPRequestCodeSerializer(OTPSerialzerMixin, serializers.ModelSerializer):
    """Serializer for processing payloads for requesting an OTP Code
    for both registration and authentication;
    """

    phone_number = PhoneNumberField(required=False)
    status = serializers.SerializerMethodField()

    class Meta:
        ref_name = "OTPRequestCodeSerializer"
        model = OneTruePairing
        fields = (
            "phone_number",
            "status",
            "usage",
            "email",
            "meta",
        )
        extra_kwargs = {
            "email": {"required": False},
            "meta": {"required": False},
        }

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if getattr(settings, "OTP_AUTH_USAGE_ONLY", False):
            extra_kwargs.setdefault("usage", {}).update(required=False)

        if not getattr(settings, "OTP_RETURN_USAGE", True):
            extra_kwargs.setdefault("usage", {}).update(write_only=True)
        return extra_kwargs

    def get_status(self, obj: OneTruePairing) -> typing.Text:
        if obj.status == OneTruePairing.Statuses.init:
            return _("The verification code was sent.")

    def _validate_usage(self, attrs):
        if (
            getattr(settings, "OTP_AUTH_USAGE_ONLY", False)
            and attrs.get("usage") != OneTruePairing.Usages.auth
        ):
            raise ValidationError(_("You can OTP only for authentication."))

    def _get_validate_user(self, attrs):
        user = get_user_model().objects.filter(self.otp_query).first()

        if attrs["usage"] == OneTruePairing.Usages.register and user:
            raise ValidationError(
                _(f"a user with this {self.otp_sub_message} already exist")
            )
        if attrs["usage"] == OneTruePairing.Usages.auth and user is None:
            raise ValidationError(_(f"Invalid {self.otp_sub_message}."))
        return user

    def _validate_old_valide_verification_code(self, attrs):
        # Validate there is unused OTP code
        timeout = now() - timedelta(seconds=getattr(settings, "OTP_TIMEOUT", 3 * 60))

        filter_kwargs = {
            "status": OneTruePairing.Statuses.init,
            "created_at__gte": timeout,
            "usage": attrs["usage"],
            **self.otp_kwargs,
        }
        if "user" in attrs:
            filter_kwargs["user"] = attrs["user"]

        if OneTruePairing.objects.filter(**filter_kwargs).exists():
            # TODO: Add a mechanism to force a new code request
            #       with additional `write_only` parameter
            logger.warning(
                f"User with this {self.otp_sub_message} requested OTP code twice."
            )
            # TODO: Add time count down
            raise serializers.ValidationError(
                _(
                    "We sent a verification code please wait for "
                    "2 minutes; before requesting a new code."
                )
            )

    def validate(self, attrs: typing.Dict) -> typing.Dict:
        attrs = super().validate(attrs)
        self._validate_usage(attrs)
        user = self._get_validate_user(attrs)
        if user:
            attrs["user"] = user
        self._validate_old_valide_verification_code(attrs)
        return attrs


class UserSerializer(serializers.Serializer):
    language = serializers.CharField(required=False)

    class Meta:
        ref_name = "UserSerializer"


class OTPVerifyCodeSerializer(OTPSerialzerMixin, serializers.ModelSerializer):
    """Serializer for processing payloads for validating
    verification codes for authentication purposes;
    """

    phone_number = PhoneNumberField(write_only=True, required=False)
    created = serializers.BooleanField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True, source="user.role")
    user = UserSerializer(required=False)

    class Meta:
        ref_name = "OTPVerifyCodeSerializer"
        model = OneTruePairing
        fields = (
            "phone_number",
            "email",
            "verification_code",
            "refresh",
            "access",
            "role",
            "created",
            "meta",
            "user",
        )
        extra_kwargs = {
            "verification_code": {"write_only": True, "required": True},
            "email": {"write_only": True, "required": False},
            "meta": {"required": False},
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if getattr(settings, "OTP_USER_SERIALIZER", None):
            module_path, class_name = settings.OTP_USER_SERIALIZER.rsplit(".", 1)
            module = import_module(module_path)
            UserSerializerClass = getattr(module, class_name)
            self.fields["user"] = UserSerializerClass(required=False)

    def validate(self, attrs: typing.Dict) -> typing.Dict:
        attrs = super().validate(attrs)

        try:
            timeout = now() - timedelta(
                seconds=getattr(settings, "OTP_TIMEOUT", 3 * 60)
            )
            instance = OneTruePairing.objects.filter(
                verification_code=attrs["verification_code"],
                status=OneTruePairing.Statuses.init,
                created_at__gte=timeout,
            ).get(self.otp_query)
            self.context["otp"] = instance
            return attrs
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(
                _(f"Invalid verification code or {self.otp_sub_message}.")
            ) from e

    def create(self, validated_data: typing.Dict) -> OneTruePairing:
        instance = self.context["otp"]
        instance.mark_used()
        user = instance.user
        instance.created = False
        if not (user or getattr(settings, "OTP_AUTH_USAGE_ONLY", False)):
            instance.created = True
            validated_data.pop(
                "verification_code",
            )
            user_data = {**validated_data.pop("user", {}), **validated_data}
            user = get_user_model().objects.create(**user_data)
            instance.user = user
            instance.save()
        # TODO: Create Generic Provider for Authentication backends
        refresh = RefreshToken.for_user(user)
        instance.refresh = str(refresh)
        instance.access = str(refresh.access_token)
        return instance

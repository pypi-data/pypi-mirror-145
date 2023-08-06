## OBytes Django OTP App

[![Build & Test](https://github.com/obytes/ob-dj-otp/workflows/Build%20&%20Test/badge.svg)](https://github.com/obytes/ob-dj-otp/actions)
[![pypi](https://img.shields.io/pypi/v/ob-dj-otp.svg)](https://pypi.python.org/pypi/ob-dj-otp)
[![license](https://img.shields.io/badge/License-BSD%203%20Clause-green.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![downloads](https://pepy.tech/badge/ob-dj-otp)](https://pepy.tech/project/ob-dj-otp)
[![python](https://img.shields.io/pypi/pyversions/ob-dj-otp.svg)](https://pypi.python.org/pypi/ob-dj-otp)
[![docs](https://github.com/obytes/ob-dj-otp/workflows/Docs/badge.svg)](https://github.com/obytes/ob-dj-otp/blob/main/docs/source/index.rst)
[![health-check](https://snyk.io/advisor/python/ob-dj-otp/badge.svg)](https://snyk.io/advisor/python/ob-dj-otp)

OTP is a Django app to conduct Web-based one true pairing, for authentication, registration and changing phone number.

## Quick start

1. Install `ob_dj_otp` latest version `pip install ob_dj_otp`

2. Add "ob_dj_otp" to your `INSTALLED_APPS` setting like this:

```python
   # settings.py
   INSTALLED_APPS = [
        ...
        "ob_dj_otp.core.otp",
   ]
```


3. Include the OTP URLs in your project urls.py like this::

```python
    # urls.py
    path("otp/", include("ob_dj_otp.apis.otp.urls")),
```

4. Run ``python manage.py migrate`` to create the otp models.


## Configuration

`OTP_FORCE_CODE` Force using this code instead of generating random one, by default it's not setted

`OTP_RETURN_USAGE` Boolean that determine whether you want to usage in the response, by default is False

`OTP_TIMEOUT` Number of seconds for the code expirations, by default it's 3 minuts

`OTP_USER_SERIALIZER` For the registration purpuse, you need to specify th path to you user serializer so you can create the user with full data

`OTP_AUTH_USAGE_ONLY` Boolean that deactivate the registration

`OTP_EMAIL_AS_PRIMARY_FIELD` Boolean to make email required

`OTP_PHONE_NUMBER_AS_PRIMARY_FIELD` Boolean to make phone number required

`SERIALIZERS_MIXIN` Dict contain mixins paths to customize serializers behavior ( see [tests](https://github.com/obytes/ob-dj-otp/blob/main/tests/apis/otp/test_custom_serializer.py) for better overview)

## Notifications
Since each project need it custom provider, the notification part should be sone on the project level not the package level, and it can be done easely but `post_save` on `OneTruePairing` model.

## Developer Guide

1. Clone github repo `git clone [url]`

2. `pipenv install --dev`

3. `pre-commit install`

4. Run unit tests `pytest`



# WebCase django JWT authentication

Based on [djangorestframework-simplejwt](https://pypi.org/project/djangorestframework-simplejwt/) with a little bit of additional goodies.

Us it's documentation as a source of truth. All changes and additional info about configuration are described here, in this documentation.

## Installation

```sh
pip install wc-django-jwt
```

In `settings.py`:

```python
INSTALLED_APPS += [
  'rest_framework_simplejwt',

  'wcd_jwt',
]

WCD_JWT = {
  # Serializer class for JWT token.
  "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
  # Serializer class for JWT token refresh.
  "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",

  # Authentication class that will be used by auth middleware to check tokens.
  "AUTHENTICATION_CLASS": "rest_framework_simplejwt.authentication.JWTAuthentication",
}

MIDDLEWARE = [
  ...
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  ...
  # Authentication middleware must be placed after django's
  # `AuthenticationMiddleware`.
  'wcd_jwt.middleware.AuthenticationMiddleware',
  ...
]
```

There are ready for use frontend for django rest framework. It mostly provided by `djangorestframework-simplejwt` with some additional changes.

In `urls.py`:

```python
from wcd_jwt.views import make_urlpatterns as jwt_make_urlpatterns

urlpatters = [
  ...
  path(
    'api/v1/auth/token/',
    include((jwt_make_urlpatterns(), 'wcd_jwt'),
    namespace='jwt-auth')
  ),
]
```

And after all that manipulations you end up with 4 views for jwt tokens authentication.

Function `make_urlpatterns` can take your custom views and replace default ones.

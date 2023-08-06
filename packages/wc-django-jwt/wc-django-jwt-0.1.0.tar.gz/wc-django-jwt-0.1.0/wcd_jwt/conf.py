from dataclasses import dataclass, field
from typing import Dict, TYPE_CHECKING
from px_settings.contrib.django import settings as s


__all__ = 'Settings', 'settings',


def get_simplejwt_setting(key: str):
    from rest_framework_simplejwt.settings import api_settings

    return getattr(api_settings, key)


@s('WCD_JWT')
@dataclass
class Settings:
    """
    Example:

    ```python
    WCD_JWT = {
        "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
        "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    }
    ```
    """
    TOKEN_OBTAIN_SERIALIZER: str = field(
        default_factory=lambda: get_simplejwt_setting('TOKEN_OBTAIN_SERIALIZER')
    )
    TOKEN_REFRESH_SERIALIZER: str = field(
        default_factory=lambda: get_simplejwt_setting('TOKEN_REFRESH_SERIALIZER')
    )

    AUTHENTICATION_CLASS: str = 'rest_framework_simplejwt.authentication.JWTAuthentication'


settings = Settings()

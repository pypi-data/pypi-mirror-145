from django.urls import path
from django.contrib.auth import login
from rest_framework_simplejwt.views import (
    TokenViewBase as _TokenViewBase, TokenVerifyView, TokenBlacklistView,
    token_verify as token_verify_view, token_blacklist as token_blacklist_view,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status

from .conf import settings


__all__ = (
    'TokenRefreshView', 'TokenObtainView', 'TokenVerifyView',
    'TokenBlacklistView',
    'token_refresh_view', 'token_obtain_view',
    'token_verify_view', 'token_blacklist_view',
    'make_urlpatterns',
)


class TokenViewBase(_TokenViewBase):
    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)

        try:
            self.serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(
            self.serializer.validated_data, status=status.HTTP_200_OK,
        )


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = settings.TOKEN_REFRESH_SERIALIZER


class TokenObtainView(TokenViewBase):
    """
    Takes a set of user credentials and returns a JSON web token to prove the
    authentication of those credentials.
    """

    _serializer_class = settings.TOKEN_OBTAIN_SERIALIZER


class WithSessionTokenObtainView(TokenObtainView):
    """
    Takes a set of user credentials and returns a JSON web token to prove the
    authentication of those credentials.
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if self.serializer.is_valid():
            login(request, self.serializer.user)

        return response


token_refresh_view = TokenRefreshView.as_view()
token_obtain_view = TokenObtainView.as_view()
with_session_token_obtain_view = WithSessionTokenObtainView.as_view()


def make_urlpatterns(
    obtain_view=with_session_token_obtain_view,
    refresh_view=token_refresh_view,
    verify_view=token_verify_view,
    blacklist_view=token_blacklist_view,
):
    return [
        path('obtain/', obtain_view, name='obtain'),
        path('refresh/', refresh_view, name='refresh'),
        path('verify/', verify_view, name='verify'),
        path('blacklist/', blacklist_view, name='blacklist'),
    ]

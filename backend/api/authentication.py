import jwt

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class DummyUser:
    """Minimal user-like object that satisfies DRF's IsAuthenticated without a DB lookup."""
    is_authenticated = True

    def __init__(self, sub):
        self.sub = sub


class LocalJWTAuthentication(BaseAuthentication):
    def authenticate_header(self, request):
        return 'Bearer realm="api"'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header[len('Bearer '):]
        try:
            payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=['RS256'])
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        username = payload.get('sub', '').replace('|', '.')
        if not username:
            raise AuthenticationFailed('Token missing sub claim')

        return (DummyUser(sub=username), token)

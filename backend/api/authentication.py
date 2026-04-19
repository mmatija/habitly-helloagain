import jwt

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


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

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, token)

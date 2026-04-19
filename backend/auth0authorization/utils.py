from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

import auth_config

import json
import jwt
import requests


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username

def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format(auth_config.AUTH0_DOMAIN)).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    
    if public_key is None:
        raise Exception('Public key not found.')
    
    issuer = 'https://{}/'.format(auth_config.AUTH0_DOMAIN)
    return jwt.decode(token, public_key, audience=auth_config.API_IDENTIFIER, issuer=issuer, algorithms=['RS256'])


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




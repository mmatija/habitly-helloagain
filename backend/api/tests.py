import jwt
import datetime
from django.test import TestCase, override_settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from api.authentication import LocalJWTAuthentication

# Pre-generated 512-bit RSA key pairs for testing only — not used in production.
TEST_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIBOQIBAAJBALi9i9aYA1ktUOE2oYFq7M0V8RWe84gCALAj0DxnFiOfJ3pTDxZ1
JA+ag6gFCCWtiKMSjDwkDX6C6bK87hdnFU8CAwEAAQJAKCHdKAAb8hp7EIHKsg+l
Y6QZnGXMZ8ZvmdQd35FRaOlCr2CuZ8xVAOicscttVAg3h9Gbwc87WxDwEu+bGCHp
SQIhANvCOJXNj0ysjBJiNFS6Ds1hfe0EcAOvVzwYdsqMATATAiEA1zTsUdM7mQqY
YmB6tkVq/TYEHR2BM8EanIEyIAZfRVUCIF4QYFAe0LutD7e+uU+a5EMc+928DIZH
QzvB7Pb9vnRpAiBejVgPE1mqAee1wWHo11MMcUEZca8kiAEjJfhZ7bLKCQIgLxOO
z9hpXeSZNT8EItIn6Ah7rEFlQMok9JJH7dE4Zhc=
-----END RSA PRIVATE KEY-----"""

TEST_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALi9i9aYA1ktUOE2oYFq7M0V8RWe84gC
ALAj0DxnFiOfJ3pTDxZ1JA+ag6gFCCWtiKMSjDwkDX6C6bK87hdnFU8CAwEAAQ==
-----END PUBLIC KEY-----"""

# A second private key whose public key is NOT trusted — used to test rejection.
MALICIOUS_PARTY_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIBOgIBAAJBAMceiF+f5l0JJbsPxVTIoMKbAE7RMLVTC2Px6bP1ZdlNnTVh3153
I3C3d2q6T/Z2pZ3btCnS5KmM9jMEFJEOs7sCAwEAAQJAJ/1f0iSg9UpjA4CVVwO8
FZlfpHSq3Z/CB96L2xKL0+pBiAF+8WsNPyiYYX+hlXPruIoviWxvzoFgx+Nm5+wQ
sQIhAPWd1VPPL/MOe1V/Z7FvDMA9JwLhDvrCw1I8f05C5Yw/AiEAz4l8dgfARXaf
GksEIx4VHEGqYe+lbmBJrH8NucD5aYUCIQDncFQl5uMtyoWY6LaS0StYscbixaNR
0tgt02e6HPskDQIgELBHl94rsepGBQE/ReunWuxU3Sc+MFAB3KMi4WsJI1kCIDmh
Ycyk7urlrUPUFph3+CZPwKZ4ypU375rnj7rdErJM
-----END RSA PRIVATE KEY-----"""


def make_token(private_key=None, exp=None):
    private_key = private_key or TEST_PRIVATE_KEY
    if exp is None:
        exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    payload = {'sub': 'testuser', 'exp': exp}
    token = jwt.encode(payload, private_key, algorithm='RS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


@api_view(['GET'])
@authentication_classes([LocalJWTAuthentication])
@permission_classes([IsAuthenticated])
def _protected_view(request):
    return Response({'ok': True})


@override_settings(JWT_PUBLIC_KEY=TEST_PUBLIC_KEY)
class LocalJWTAuthenticationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_rejects_request_without_token(self):
        request = self.factory.get('/')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 401)

    def test_rejects_token_signed_with_unknown_key(self):
        token = make_token(private_key=MALICIOUS_PARTY_PRIVATE_KEY)
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 401)

    def test_rejects_expired_token(self):
        token = make_token(exp=datetime.datetime(2000, 1, 1))
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 401)

    def test_accepts_token_signed_with_trusted_key(self):
        token = make_token()
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 200)

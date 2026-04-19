import jwt
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

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


def make_token(private_key=None):
    private_key = private_key or TEST_PRIVATE_KEY
    token = jwt.encode({'sub': 'testuser'}, private_key, algorithm='RS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


@override_settings(JWT_PUBLIC_KEY=TEST_PUBLIC_KEY)
class HelloEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_hello_returns_401_without_token(self):
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, 401)

    def test_hello_returns_401_with_wrong_key(self):
        token = make_token(private_key=MALICIOUS_PARTY_PRIVATE_KEY)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, 401)

    def test_hello_returns_200_with_valid_token(self):
        token = make_token()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, world!'})

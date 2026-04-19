import datetime
from django.test import TestCase, override_settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from api.authentication import LocalJWTAuthentication
from api.fixtures import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY
from api.tokens import generate_token

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

@api_view(['GET'])
@authentication_classes([LocalJWTAuthentication])
@permission_classes([IsAuthenticated])
def _protected_view(request):
    return Response({'ok': True})


@override_settings(JWT_PRIVATE_KEY=TEST_PRIVATE_KEY, JWT_PUBLIC_KEY=TEST_PUBLIC_KEY)
class LocalJWTAuthenticationTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_rejects_request_without_token(self):
        request = self.factory.get('/')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 401)

    @override_settings(JWT_PRIVATE_KEY=MALICIOUS_PARTY_PRIVATE_KEY)
    def test_rejects_token_signed_with_unknown_key(self):
        token = generate_token('testuser')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 401)

    def test_rejects_expired_token(self):
        past = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
        token = generate_token('testuser', exp=past)
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 401)

    def test_accepts_token_signed_with_trusted_key(self):
        token = generate_token('testuser')
        request = self.factory.get('/', HTTP_AUTHORIZATION=f'Bearer {token}')
        response = _protected_view(request)
        self.assertEqual(response.status_code, 200)


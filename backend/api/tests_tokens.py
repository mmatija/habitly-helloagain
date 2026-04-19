import jwt
import datetime
from django.test import TestCase, override_settings
from api.fixtures import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY
from api.tokens import generate_token


@override_settings(JWT_PRIVATE_KEY=TEST_PRIVATE_KEY, JWT_PUBLIC_KEY=TEST_PUBLIC_KEY)
class GenerateTokenTests(TestCase):
    def test_token_has_correct_subject(self):
        token = generate_token('alice')
        payload = jwt.decode(token, TEST_PUBLIC_KEY, algorithms=['RS256'])
        self.assertEqual(payload['sub'], 'alice')

    def test_token_expires_in_24_hours_by_default(self):
        before = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        token = generate_token('alice')
        after = datetime.datetime.now(datetime.timezone.utc)

        payload = jwt.decode(token, TEST_PUBLIC_KEY, algorithms=['RS256'])
        exp = datetime.datetime.fromtimestamp(payload['exp'], tz=datetime.timezone.utc)

        self.assertGreaterEqual(exp, before + datetime.timedelta(hours=24))
        self.assertLessEqual(exp, after + datetime.timedelta(hours=24))

    def test_token_uses_custom_expiration(self):
        custom_exp = datetime.datetime(2030, 6, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        token = generate_token('alice', exp=custom_exp)

        payload = jwt.decode(token, TEST_PUBLIC_KEY, algorithms=['RS256'])
        exp = datetime.datetime.fromtimestamp(payload['exp'], tz=datetime.timezone.utc)

        self.assertEqual(exp, custom_exp)

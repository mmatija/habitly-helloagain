import datetime
import jwt

from django.conf import settings


def generate_token(username, exp=None):
    if exp is None:
        exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    payload = {
        'sub': username,
        'exp': exp,
    }
    token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm='RS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

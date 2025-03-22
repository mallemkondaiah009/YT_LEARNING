
# accounts/tokens.py
import time
from django.utils.crypto import salted_hmac
import six

class CustomTokenGenerator:
    def make_token(self, user):
        timestamp = str(int(time.time()))
        key_salt = "custom_token_generator"
        value = six.text_type(user.pk) + user.email + timestamp
        token = salted_hmac(key_salt, value).hexdigest()[::2] + timestamp
        print(f"Generated token for user {user.pk}: {token}")  # Debug
        return token

    def check_token(self, user, token):
        if not (user and token):
            return False
        
        # Extract timestamp (last 10 characters)
        timestamp = token[-10:]
        try:
            ts = int(timestamp)
        except ValueError:
            print(f"Invalid timestamp in token: {token}")  # Debug
            return False

        # Check expiration (24 hours)
        if (int(time.time()) - ts) > (24 * 60 * 60):
            print(f"Token expired: {token}, time difference: {int(time.time()) - ts}")  # Debug
            return False

        # Regenerate token to compare
        key_salt = "custom_token_generator"
        value = six.text_type(user.pk) + user.email + timestamp
        expected_token = salted_hmac(key_salt, value).hexdigest()[::2] + timestamp
        print(f"Checking token: {token} vs Expected: {expected_token}")  # Debug
        return expected_token == token

custom_token_generator = CustomTokenGenerator()
from django.contrib.auth.models import User

def save_google_email(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2' and user:
        email = response.get('email', '').lower()
        if email and not user.email:
            user.email = email
            user.save()
        elif email and user.email != email:
            # Handle email mismatch if needed
            user.email = email
            user.save()

SOCIALACCOUNT_PIPELINE = (
    'accounts.pipeline.save_google_email',
)

SOCIAL_AUTH_PIPELINE = (
    'accounts.pipeline.save_google_email',
)
# signals.py
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in

def store_user_data_in_session(request, sociallogin):
    """Helper function to store user data in session"""
    if sociallogin and hasattr(sociallogin, 'account'):
        user_data = sociallogin.account.extra_data
        
        # Store selected user data in session
        session_data = {
            'user_id': user_data.get('id'),
            'email': user_data.get('email'),
            'username': user_data.get('name'),
            'first_name': user_data.get('given_name'),
            'last_name': user_data.get('family_name'),
            'picture': user_data.get('picture'),
        }
        

        
        request.session['user_data'] = session_data
        # Set session expiry (0 = until browser closes, or set specific time in seconds)
        request.session.set_expiry(0)
    else:
        # Clear session data if no sociallogin
        request.session.pop('user_data', None)

@receiver(user_signed_up)
def handle_user_signed_up(request, sociallogin, user, **kwargs):
    """Handle new user signup via Google"""
    store_user_data_in_session(request, sociallogin)

@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    """Handle user login via Google"""
    # sociallogin is only present in kwargs if it's a social login
    sociallogin = kwargs.get('sociallogin')
    store_user_data_in_session(request, sociallogin)
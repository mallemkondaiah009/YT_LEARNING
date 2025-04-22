from django.conf import settings
from django.shortcuts import redirect
from functools import wraps
from django.urls import reverse

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            login_url = f"{reverse('login')}?next={request.path}"
            return redirect(login_url)
        return view_func(request, *args, **kwargs)
    return wrapper
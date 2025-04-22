from django.utils import timezone
from .models import UserStreak
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

class StreakMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Use request.user for the authenticated user
        if request.user.is_authenticated:
            try:
                streak, _ = UserStreak.objects.get_or_create(user=request.user)
                streak.update_streak()
            except Exception:
                pass  # Handle any potential database errors silently

        response = self.get_response(request)
        return response
# middleware.py
from django.utils import timezone
from .models import UserStreak, UserRegistrations

class StreakMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            try:
                user = UserRegistrations.objects.get(id=user_id)
                streak, _ = UserStreak.objects.get_or_create(user=user)
                streak.update_streak()
            except UserRegistrations.DoesNotExist:
                pass
        
        response = self.get_response(request)
        return response
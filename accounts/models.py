from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

    
class UserStreak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    streak_count = models.IntegerField(default=0)
    last_visit = models.DateTimeField(null=True, blank=True)
    longest_streak = models.IntegerField(default=0)

    def update_streak(self):
        now = timezone.now()
        if self.last_visit:
            days_diff = (now.date() - self.last_visit.date()).days
            if days_diff == 0:
                return
            elif days_diff == 1:
                self.streak_count += 1
            elif days_diff > 1:
                self.streak_count = 1
            self.longest_streak = max(self.longest_streak, self.streak_count)
        else:
            self.streak_count = 1
        
        self.last_visit = now
        self.save()
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    coins = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class ScheduledReward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    execute_at = models.DateTimeField()

    def __str__(self):
        return f"Scheduled: {self.user.username} → {self.amount} coins at {self.execute_at}"


class RewardLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    given_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log: {self.user.username} ← {self.amount} coins"

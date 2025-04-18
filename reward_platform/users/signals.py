from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import ScheduledReward
from .tasks import process_scheduled_reward
from datetime import timedelta

@receiver(post_save, sender=ScheduledReward)
def schedule_reward_task(sender, instance, created, **kwargs):
    if created:
        delay = (instance.execute_at - now()).total_seconds()
        process_scheduled_reward.apply_async((instance.id,), countdown=delay)

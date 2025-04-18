from celery import shared_task
from django.utils import timezone
from .models import ScheduledReward, RewardLog

@shared_task
def process_scheduled_reward(reward_id):
    try:
        reward = ScheduledReward.objects.get(id=reward_id)
        
        # Check if the reward hasn't been processed yet
        if not reward.user.coins:
            # Update user's coins
            reward.user.coins += reward.amount
            reward.user.save()
            
            # Create reward log
            RewardLog.objects.create(
                user=reward.user,
                amount=reward.amount
            )
            
            # Delete the scheduled reward
            reward.delete()
            
            return f"Successfully processed reward {reward_id}"
    except ScheduledReward.DoesNotExist:
        return f"Reward {reward_id} not found"

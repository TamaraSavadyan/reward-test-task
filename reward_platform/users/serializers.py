from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ScheduledReward, RewardLog

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'coins')

class ScheduledRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReward
        fields = ('id', 'amount', 'execute_at')
        read_only_fields = ('id',)

class RewardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardLog
        fields = ('amount', 'given_at')
        read_only_fields = ('given_at',)

class RequestRewardSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)

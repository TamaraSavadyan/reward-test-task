from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import ScheduledReward, RewardLog
from .serializers import (
    UserProfileSerializer,
    ScheduledRewardSerializer,
    RewardLogSerializer,
    RequestRewardSerializer
)
from .tasks import process_scheduled_reward

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class RewardListView(generics.ListAPIView):
    serializer_class = RewardLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RewardLog.objects.filter(user=self.request.user).order_by('-given_at')

class RequestRewardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = RequestRewardSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            
            # Check if user has requested a reward in the last 24 hours
            last_reward = ScheduledReward.objects.filter(
                user=request.user,
                execute_at__gte=timezone.now() - timedelta(days=1)
            ).first()
            
            if last_reward:
                return Response(
                    {"error": "You can only request one reward per day"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create scheduled reward for 5 minutes from now
            execute_at = timezone.now() + timedelta(minutes=5)
            scheduled_reward = ScheduledReward.objects.create(
                user=request.user,
                amount=amount,
                execute_at=execute_at
            )

            # Schedule Celery task
            process_scheduled_reward.apply_async(
                args=[scheduled_reward.id],
                eta=execute_at
            )

            return Response(
                {"message": f"Reward of {amount} coins will be given in 5 minutes"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

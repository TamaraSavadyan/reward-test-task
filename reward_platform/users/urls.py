from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import UserProfileView, RewardListView, RequestRewardView

urlpatterns = [
    # JWT endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Profile and rewards endpoints
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('rewards/', RewardListView.as_view(), name='reward-list'),
    path('rewards/request/', RequestRewardView.as_view(), name='request-reward'),
]

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import ScheduledReward, RewardLog
from .tasks import process_scheduled_reward

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(
        username='perftestuser',
        password='testpass123',
        email='perftest@example.com'
    )
    return user

@pytest.fixture
def auth_token(api_client, authenticated_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'perftestuser',
        'password': 'testpass123'
    }, format='json')
    return response.data['access']

@pytest.mark.benchmark(
    group="authentication",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    warmup=True
)
def test_token_obtain_performance(benchmark, api_client):
    url = reverse('token_obtain_pair')
    data = {
        'username': 'perftestuser',
        'password': 'testpass123'
    }
    
    def token_obtain():
        return api_client.post(url, data, format='json')
    
    result = benchmark(token_obtain)
    assert result.status_code == 200

@pytest.mark.benchmark(
    group="api-endpoints",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    warmup=True
)
def test_profile_endpoint_performance(benchmark, api_client, auth_token):
    url = reverse('user-profile')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    
    def get_profile():
        return api_client.get(url)
    
    result = benchmark(get_profile)
    assert result.status_code == 200

@pytest.mark.benchmark(
    group="api-endpoints",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    warmup=True
)
def test_reward_list_performance(benchmark, api_client, auth_token, authenticated_user):
    # Create some reward logs for testing
    for _ in range(100):
        RewardLog.objects.create(user=authenticated_user, amount=10)
    
    url = reverse('reward-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    
    def get_rewards():
        return api_client.get(url)
    
    result = benchmark(get_rewards)
    assert result.status_code == 200

@pytest.mark.benchmark(
    group="celery-tasks",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    warmup=True
)
def test_scheduled_reward_processing_performance(benchmark, authenticated_user):
    def create_and_process_reward():
        reward = ScheduledReward.objects.create(
            user=authenticated_user,
            amount=10,
            execute_at=timezone.now()
        )
        return process_scheduled_reward(reward.id)
    
    result = benchmark(create_and_process_reward)
    assert result is not None

@pytest.mark.benchmark(
    group="concurrent-requests",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    warmup=True
)
def test_concurrent_reward_requests_performance(benchmark, api_client, auth_token):
    url = reverse('request-reward')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {auth_token}')
    
    def request_reward():
        return api_client.post(url, {'amount': 10}, format='json')
    
    # Run multiple concurrent requests
    results = benchmark.pedantic(
        request_reward,
        rounds=10,
        iterations=5
    )
    assert all(r.status_code in (201, 400) for r in results)

@pytest.mark.benchmark(
    group="database-operations",
    min_time=0.1,
    max_time=0.5,
    min_rounds=5,
    warmup=True
)
def test_bulk_reward_log_creation_performance(benchmark, authenticated_user):
    def create_reward_logs():
        RewardLog.objects.bulk_create([
            RewardLog(user=authenticated_user, amount=10)
            for _ in range(100)
        ])
    
    benchmark(create_reward_logs)
    assert RewardLog.objects.count() >= 100 
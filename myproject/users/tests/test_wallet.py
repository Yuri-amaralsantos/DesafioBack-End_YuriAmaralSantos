import pytest
from django.contrib.auth.models import User
from users.models import Wallet
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_wallet_creation():
    """Criar carteira do usuário"""
    user = User.objects.create_user(username="walletuser", password="securepassword")
    wallet = Wallet.objects.create(user=user, balance=100)
    assert wallet.balance == 100

@pytest.mark.django_db
def test_get_wallet_balance():
    """Ver carteira do usuário logado"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet, _ = Wallet.objects.get_or_create(user=user, balance=200)


    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/wallet/")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["balance"] == 200

@pytest.mark.django_db
def test_update_wallet_balance():
    """Atualizar carteira"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    wallet = Wallet.objects.create(user=user, balance=100)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/wallet/update/", {"amount": 50}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["balance"] == 150  

@pytest.mark.django_db
def test_update_wallet_invalid_amount():
    """Atualizar carteira com valor invalido"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    Wallet.objects.create(user=user, balance=100)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/api/wallet/update/", {"amount": "invalid"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid amount"

@pytest.mark.django_db
def test_get_other_user_wallet():
    """Ver carteira de outro usuário"""
    user1 = User.objects.create_user(username="user1", password="password1")
    user2 = User.objects.create_user(username="user2", password="password2")

    Wallet.objects.create(user=user1, balance=300)

    Wallet.objects.create(user=user2, balance=500)

    client = APIClient()
    client.force_authenticate(user=user1)

    response = client.get(f"/api/wallet/{user2.username}/")

    assert response.status_code == status.HTTP_200_OK
    print(response.data)
    assert response.data["balance"] == 500





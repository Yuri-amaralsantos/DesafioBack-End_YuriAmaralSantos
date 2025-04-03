import pytest
from django.contrib.auth.models import User
from users.models import Wallet, Transfer
from rest_framework.test import APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta

@pytest.mark.django_db
def test_successful_transfer():
    """Transferir valores entre dois usuários"""
    sender = User.objects.create_user(username="sender", password="password")
    recipient = User.objects.create_user(username="recipient", password="password")

    sender_wallet = Wallet.objects.create(user=sender, balance=500)
    recipient_wallet = Wallet.objects.create(user=recipient, balance=100)

    client = APIClient()
    client.force_authenticate(user=sender)

    response = client.post("/api/transfer/", {"recipient": "recipient", "amount": 200}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Transfer successful"
    assert response.data["new_balance"] == 300 

    sender_wallet.refresh_from_db()
    recipient_wallet.refresh_from_db()

    assert sender_wallet.balance == 300
    assert recipient_wallet.balance == 300  

@pytest.mark.django_db
def test_transfer_insufficient_balance():
    """Transferir sem saldo."""
    sender = User.objects.create_user(username="sender", password="password")
    recipient = User.objects.create_user(username="recipient", password="password")

    Wallet.objects.create(user=sender, balance=50)  
    Wallet.objects.create(user=recipient, balance=100)

    client = APIClient()
    client.force_authenticate(user=sender)

    response = client.post("/api/transfer/", {"recipient": "recipient", "amount": 200}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Insufficient balance."

@pytest.mark.django_db
def test_transfer_to_nonexistent_user():
    """Transferir para usuário que não existe."""
    sender = User.objects.create_user(username="sender", password="password")
    Wallet.objects.create(user=sender, balance=300)

    client = APIClient()
    client.force_authenticate(user=sender)

    response = client.post("/api/transfer/", {"recipient": "nonexistent", "amount": 100}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "Recipient user not found."


@pytest.mark.django_db
def test_transfer_invalid_amount():
    """Transferir com um valor invalido ou zero"""
    sender = User.objects.create_user(username="sender", password="password")
    recipient = User.objects.create_user(username="recipient", password="password")

    Wallet.objects.create(user=sender, balance=500)
    Wallet.objects.create(user=recipient, balance=100)

    client = APIClient()
    client.force_authenticate(user=sender)

 
    response_negative = client.post("/api/transfer/", {"recipient": "recipient", "amount": -50}, format="json")
    assert response_negative.status_code == status.HTTP_400_BAD_REQUEST
    assert response_negative.data["error"] == "Amount must be greater than zero."


    response_zero = client.post("/api/transfer/", {"recipient": "recipient", "amount": 0}, format="json")
    assert response_zero.status_code == status.HTTP_400_BAD_REQUEST
    assert response_zero.data["error"] == "Amount must be greater than zero."

@pytest.mark.django_db
def test_transfer_non_numeric_amount():
    """Transferir com um valor não numérico."""
    sender = User.objects.create_user(username="sender", password="password")
    recipient = User.objects.create_user(username="recipient", password="password")

    Wallet.objects.create(user=sender, balance=500)
    Wallet.objects.create(user=recipient, balance=100)

    client = APIClient()
    client.force_authenticate(user=sender)

    response = client.post("/api/transfer/", {"recipient": "recipient", "amount": "invalid"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "Invalid amount."

@pytest.mark.django_db
def test_list_transfers_with_date_filter():
    """Listar por data."""
    sender = User.objects.create_user(username="sender", password="password")
    recipient = User.objects.create_user(username="recipient", password="password")

    Wallet.objects.create(user=sender, balance=500)
    Wallet.objects.create(user=recipient, balance=100)

  
    transfer1 = Transfer.objects.create(sender=sender, receiver=recipient, amount=50)
    transfer1.timestamp = now() - timedelta(days=3)
    transfer1.save()

    transfer2 = Transfer.objects.create(sender=sender, receiver=recipient, amount=100)
    transfer2.timestamp = now() - timedelta(days=1)
    transfer2.save()

    client = APIClient()
    client.force_authenticate(user=sender)

  
    response = client.get(
        f"/api/transfer/list/?start_date={(now() - timedelta(days=2)).date()}&end_date={now().date()}"
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  
    assert response.data[0]["amount"] == 100

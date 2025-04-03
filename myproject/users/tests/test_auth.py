import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

@pytest.mark.django_db
def test_create_user():
    """Criar usuário"""
    user = User.objects.create_user(username="testuser", password="testpassword")
    assert user.username == "testuser"

@pytest.mark.django_db
def test_login_user():
    """Logar e autenticar token"""

    user = User.objects.create_user(username="testuser", password="testpassword")

   
    client = APIClient()

    response = client.post("/api/login/", {"username": "testuser", "password": "testpassword"}, format="json")

  
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data  

@pytest.mark.django_db
def test_delete_user():
    """Deletar usuário."""
  
    user = User.objects.create_user(username="testuser", password="testpassword")

    
    client = APIClient()


    response = client.post("/api/login/", {"username": "testuser", "password": "testpassword"}, format="json")
    assert response.status_code == status.HTTP_200_OK

    token = response.data["access"] 

  
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

   
    delete_response = client.delete("/api/delete/")

   
    assert delete_response.status_code == status.HTTP_200_OK
    assert delete_response.data["message"] == "User deleted successfully."

 
    assert not User.objects.filter(username="testuser").exists()
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Wallet
from .models import Transfer

class UserSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(source="wallet.balance", max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'balance']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
  
        user = User.objects.create_user(**validated_data)
        
    
        Wallet.objects.create(user=user, balance=0.0)

        return user

class TransferSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username", read_only=True)
    receiver = serializers.CharField(source="receiver.username", read_only=True)

    class Meta:
        model = Transfer
        fields = ['id', 'sender', 'receiver', 'amount', 'timestamp']
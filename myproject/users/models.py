from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"

class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transfers")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_transfers")
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.amount}"

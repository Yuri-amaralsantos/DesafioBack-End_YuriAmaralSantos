from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ..models import Wallet, Transfer
from ..serializers import TransferSerializer
from django.utils.dateparse import parse_date

class TransferWalletView(APIView):
    """
    API endpoint to transfer balance from the authenticated user to another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_username = request.data.get("recipient")
        amount = request.data.get("amount")

        if not recipient_username or amount is None:
            return Response({"error": "Recipient and amount are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            if amount <= 0:
                return Response({"error": "Amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sender_wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Sender wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            recipient_user = User.objects.get(username=recipient_username)
            recipient_wallet = Wallet.objects.get(user=recipient_user)
        except User.DoesNotExist:
            return Response({"error": "Recipient user not found."}, status=status.HTTP_404_NOT_FOUND)
        except Wallet.DoesNotExist:
            return Response({"error": "Recipient wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        if sender_wallet.balance < amount:
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        sender_wallet.balance -= amount
        recipient_wallet.balance += amount
        sender_wallet.save()
        recipient_wallet.save()

        Transfer.objects.create(
            sender=request.user,
            receiver=recipient_user,
            amount=amount
        )

        return Response(
            {"message": "Transfer successful", "new_balance": sender_wallet.balance},
            status=status.HTTP_200_OK
        )


class TransferListView(generics.ListAPIView):
    """
    API endpoint to list transfers made by a user with optional date filtering.
    """
    serializer_class = TransferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transfer.objects.filter(sender=user)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(timestamp__date__gte=start_date)

        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(timestamp__date__lte=end_date)

        return queryset
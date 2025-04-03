from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ..models import Wallet

class UpdateWalletView(APIView):
    """
    API endpoint to update the user's wallet balance.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            wallet = Wallet.objects.get(user=request.user)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get("amount")
        if amount is None:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        wallet.balance += amount
        wallet.save()
        return Response({"message": "Balance updated", "balance": wallet.balance}, status=status.HTTP_200_OK)


class GetWalletBalanceView(APIView):
    """
    API endpoint to retrieve the authenticated user's wallet balance.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)


class ViewOtherUserWallet(APIView):
    """
    API endpoint to retrieve another user's wallet balance.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, name):
        try:
            user = User.objects.get(username=name)
           
            wallet, created = Wallet.objects.get_or_create(user=user)
            return Response({
                "user": user.username,
                "balance": wallet.balance
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet not found for this user."}, status=status.HTTP_404_NOT_FOUND)
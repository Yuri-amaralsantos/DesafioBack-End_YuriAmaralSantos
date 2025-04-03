from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from ..serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class RegisterUserView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class LoginView(APIView):
    """
    API endpoint para login e obtenção de tokens JWT.
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username e senha são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Credenciais inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

        
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class DeleteUserView(generics.DestroyAPIView):
    """
    API endpoint to delete the authenticated user.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({"message": "User deleted successfully."})

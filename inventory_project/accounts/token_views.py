# accounts/token_views.py
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

# Plain token endpoint (same behavior as DRF's, but permission explicit)
class CustomObtainAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

# Nice login endpoint that returns a message + token
class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get("token")
        if token:
            return Response(
                {"message": "Login successful", "token": token},
                status=status.HTTP_200_OK,
            )
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

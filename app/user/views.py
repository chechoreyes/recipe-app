"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import UserSerializzer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializzer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# RetrieveUpdateAPI is provided by DRF for updating objects in the databse
class ManageUseView(generics.RetrieveUpdateAPIView):
    """Manage the autehnticated user."""

    # Get the serializer
    serializer_class = UserSerializzer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """retrieve and return the authenticated user."""
        return self.request.user

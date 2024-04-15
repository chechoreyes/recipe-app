"""
Serialziers for the user API View
"""

from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializzer(serializers.ModelSerializer):
    """Serialzier for the user object"""

    # The Meta class provide metadata to the ModelForm or the Model class
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""

        return get_user_model().objects.create_user(**validated_data)

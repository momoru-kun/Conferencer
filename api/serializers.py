from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serialization of user"""

    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'email', 'first_name', 'last_name')
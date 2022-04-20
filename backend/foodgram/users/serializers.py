from djoser.serializers import UserCreateSerializer

from .models import User


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')

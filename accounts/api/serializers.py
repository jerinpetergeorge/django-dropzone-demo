from rest_framework import serializers

from accounts.models import User


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]

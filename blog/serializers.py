from dataclasses import field
from rest_framework import  serializers
from .models import UserPayer, Auth_token

class UserPayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayer
        fields = ('document', 'name', 'email', 'password')


class Auth_tokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth_token
        fields = ('user_payer', 'token')



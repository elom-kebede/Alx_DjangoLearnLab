from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model =  get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user =  get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Generate a token upon registration
        return user

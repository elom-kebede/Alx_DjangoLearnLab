from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token



class UserSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    class Meta:
        model =  get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers_count', 'following_count']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model =  get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user =  get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)  # Generate a token upon registration
        return user
    
    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data["username"])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            update_last_login(None, user)
            return Response({"token": token.key, "user": UserSerializer(user).data})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    

    
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the authenticated user
    


class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to follow
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        # Make sure the user is not following themselves
        if user_to_follow == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the current user's following list
        request.user.following.add(user_to_follow)

        # Return a success response
        return Response({"detail": "You are now following this user."}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        # Get the user to unfollow
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        # Remove the user from the current user's following list
        request.user.following.remove(user_to_unfollow)

        # Return a success response
        return Response({"detail": "You have unfollowed this user."}, status=status.HTTP_200_OK)




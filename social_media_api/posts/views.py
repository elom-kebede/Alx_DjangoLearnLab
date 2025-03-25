from django.shortcuts import render
from rest_framework import viewsets, permissions, filters,generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Create your views here.



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set post author to the logged-in user

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set comment author to the logged-in user


User = get_user_model()

class FeedView(generics.ListAPIView):
    

    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        following_users = request.user.following.all()

       
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        
        from .serializers import PostSerializer
        serialized_posts = PostSerializer(posts, many=True)

        return Response(serialized_posts.data, status=status.HTTP_200_OK)
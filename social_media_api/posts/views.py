from django.shortcuts import render
from rest_framework import viewsets, permissions, filters,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
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
    


class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has already liked the post
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the like
        like = Like.objects.create(user=request.user, post=post)

        # Create a notification for the post owner
        notification = Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target_ct=ContentType.objects.get_for_model(Post),
            target_id=post.id
        )

        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
    

class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"detail": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
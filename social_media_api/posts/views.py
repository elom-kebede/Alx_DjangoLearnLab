from django.shortcuts import render
from rest_framework import viewsets, permissions, filters,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
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
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, pk, format=None):
        # Fetch the post object using get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Check if the user already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        ["generics.get_object_or_404(Post, pk=pk)", "Notification.objects.create"]
        
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Create a notification for the post owner when the post is liked
            Notification.objects.create(
                recipient=post.user,  # Post owner is the recipient
                actor=request.user,  # The user who liked the post
                verb="liked your post",  # Action description
                target=post,  # Target is the post
            )
            return Response({'message': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
        else:
            # The user has already liked the post
            return Response({'message': 'You have already liked this post.'}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, pk, format=None):
        # Fetch the post object using get_object_or_404
        post = generics.get_object_or_404(Post, pk=pk)
        
        try:
            # Attempt to get the Like object and delete it
            like = Like.objects.get(user=request.user, post=post)
            like.delete()

            # Create a notification for the post owner when the post is unliked
            Notification.objects.create(
                recipient=post.user,  # Post owner is the recipient
                actor=request.user,  # The user who unliked the post
                verb="unliked your post",  # Action description
                target=post,  # Target is the post
            )

            return Response({'message': 'Post unliked successfully.'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            # If the Like object doesn't exist, the user has not liked the post yet
            return Response({'message': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)
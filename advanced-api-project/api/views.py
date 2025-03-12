from django.shortcuts import render
from rest_framework import generics, permissions,serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from datetime import datetime
from .serializers import BookSerializer
from .models import Book

# Create your views here.

class BookListView(generics.ListAPIView):
    # Retrieves all books. Available to both authenticated and unauthenticated users.
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]    # Read access for everyone

class BookDetailView(generics.RetrieveAPIView):

    #  Retrieves a single book by ID. Available to both authenticated and unauthenticated users.

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    
    #Allows authenticated users to create a new book.
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create books


    def perform_create(self, serializer):
        if serializer.validated_data['publication_year'] > datetime.now().year:
            raise serializers.ValidationError({"publication_year": "Publication year cannot be in the future."})
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    """
    Allows authenticated users to update an existing book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can update books

    def perform_update(self, serializer):
        if serializer.validated_data['publication_year'] > datetime.now().year:
            raise serializers.ValidationError({"publication_year": "Publication year cannot be in the future."})
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    """
    Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can delete books

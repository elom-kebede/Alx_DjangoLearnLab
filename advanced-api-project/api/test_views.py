from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book

class BookAPITest(TestCase):
    def setUp(self):
        """Set up test data and test client."""
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create test books
        self.book1 = Book.objects.create(title="Django for Beginners", author="William S. Vincent", publication_year=2021)
        self.book2 = Book.objects.create(title="Python Crash Course", author="Eric Matthes", publication_year=2019)

        # Authentication
        self.client.login(username="testuser", password="testpassword")

    def test_get_books_list(self):
        """Test retrieving the book list (GET /api/books/)."""
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book(self):
        """Test creating a book (POST /api/books/)."""
        book_data = {
            "title": "New Book",
            "author": "New Author",
            "publication_year": 2022
        }
        response = self.client.post("/api/books/", book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        """Test updating a book (PUT /api/books/{id}/)."""
        book_data = {
            "title": "Updated Title",
            "author": self.book1.author,
            "publication_year": self.book1.publication_year
        }
        response = self.client.put(f"/api/books/{self.book1.id}/", book_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        """Test deleting a book (DELETE /api/books/{id}/)."""
        response = self.client.delete(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        response = self.client.get("/api/books/?author=William S. Vincent")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """Test searching for books by title."""
        response = self.client.get("/api/books/?search=Django")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        """Test ordering books by publication year."""
        response = self.client.get("/api/books/?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Python Crash Course")  # Oldest book first


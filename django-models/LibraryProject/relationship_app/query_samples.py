from relationship_app.models import Author, Book, Library, Librarian

from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Get all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    for book in books:
        print(f"Book Title: {book.title}")

# Query 2: List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    for book in books:
        print(f"Book Title: {book.title}")

# Query 3: Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    print(f"Librarian: {librarian.name}")

# Example usage
if __name__ == '__main__':
    print("Books by Author 'John Doe':")
    books_by_author('John Doe')

    print("\nBooks in Library 'Central Library':")
    books_in_library('Central Library')

    print("\nLibrarian for 'Central Library':")
    librarian_for_library('Central Library')
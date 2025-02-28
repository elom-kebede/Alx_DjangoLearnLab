from .models import Book
from django.views.generic.detail import DetailView
from .models import Library
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .forms import BookForm

# Create your views here.

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# Login View
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'  # Specify your template here


# Logout View
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'  # Specify your template here


# Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


def admin_check(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(admin_check)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


def librarian_check(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(librarian_check)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


def member_check(user):
    return user.userprofile.role == 'Member'

@user_passes_test(member_check)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# Add a new book (requires can_add_book permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Assuming you have a book list view
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

# Edit an existing book (requires can_change_book permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form})

# Delete a book (requires can_delete_book permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'confirm_delete.html', {'book': book})
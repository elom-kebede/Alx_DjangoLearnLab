from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']  # Include the fields you want to display in the form
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if '<script>' in title:  # Basic XSS prevention
            raise forms.ValidationError("Invalid input detected.")
        return title
from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

# writing the book serializer

class BookSerializer(serializers.ModelSerializer):

    def validate_publication_year(self, value): # to check the year not to be the future
        current_year = datetime.now().year
        if value > current_year :
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
    class Meta:
        model = Book
        fields = '__all__' 

# serializer for the author    
class AuthorSerializer(serializers.ModelSerializer):

    books = BookSerializer(many=True, read_only=True) #nested serialization
                          

    class Meta:
        model = Author
        fields = ['name' , 'books']




    
from rest_framework import serializers
from .models import Book, Author
from datetime import datetime

# writing the book serializer
class BookSerializers(serializers.ModelSerializer):

    def validate_publication_year(self, value): # to check the year not to be the future
        current_year = datetime.now().year
        if value > current_year :
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
    class meta:
        model = Book
        fields = '_all_'


# serializer for the author    
class AuthorSerializers(serializers.ModelSerializer):

    books = BookSerializers(many = True , ready_only=True) #nested serialization

    class meta:
        model = Author
        fields = '[name , books]'




    
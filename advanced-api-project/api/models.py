from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)

    def _str_(self):
     return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)

    def _str_(self):
       return self.title

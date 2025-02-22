# Retrieve Operation

**Command:**

book = Book.objects.get(title="1984")

# expected outPut

>>> book
<Book: 1984>
>>> book.author
'George Orwell'
>>> book.publication_year
1949

from .serializers import BookSerializer
from rest_framework import generics
from .models import Book
from django.shortcuts import render
from .management.commands.scrape_books import  *
from cryptography.fernet import Fernet

# Generate a new Fernet key (you can run this in Python shell)
# fernet_key = Fernet.generate_key()
# # print("this is an fernet",fernet)
# print('this is fernet_key',fernet_key.decode())

# # Encrypt and Decrypt Functions
# def encrypt_data(data, key):
#     fernet = Fernet(key)
#     encrypted_data = fernet.encrypt(data.encode())  # Ensure data is in bytes
#     return encrypted_data
#
#
# def decrypt_data(encrypted_data, key):
#     fernet = Fernet(key)
#     decrypted_data = fernet.decrypt(encrypted_data).decode()  # Decode back to string
#     return decrypted_data

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def all_records(request):
    # Retrieve all books from the database
    books = Book.objects.all()

    # Decrypt the necessary fields before passing the data to the template
    decrypted_books = []
    for book in books:
        print("Encrypted Book Data:", book.encrypt_value)
        decrypted_book = book.get_decrypted_fields()
        print("Decrypted Book Data:", decrypted_book)# Decrypt the fields using the method you created
        decrypted_books.append(decrypted_book)
    # Pass the decrypted data to the template
    context = {
        "data": decrypted_books,
    }
    print('decrypted books are :',decrypted_books)
    return render(request, 'table.html', context)


def base(request):
    return render(request,'base.html')

def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            category__icontains=query
        ) | Book.objects.filter(
            description__icontains=query
        )
    else:
        books = []
    return render(request, 'searched_records.html', {'books': books, 'query': query})


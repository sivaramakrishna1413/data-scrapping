from django.contrib import admin
from .management.commands.scrape_books import scrape_and_import_books
from .views import BookList
from django.urls import path
from . import views
from .views import BookListCreateView, BookRetrieveUpdateDestroyView
# from data_app.management.commands.scrape_books import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("books/",BookList.as_view(),name="book-list"),
    path('books/create/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-retrieve-update-destroy'),
    path('scrape-books/', scrape_and_import_books, name='scrape_books'),
    path('',views.all_records,name='book_records'),
    path('base/main/',views.base,name='base_file'),
    path('search/books/',views.search_books,name='searchBook')

]

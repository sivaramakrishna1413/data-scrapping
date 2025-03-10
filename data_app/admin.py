from django.contrib import admin
from .models import Book

# Register the Book model to make it available in the admin interface
admin.site.register(Book)

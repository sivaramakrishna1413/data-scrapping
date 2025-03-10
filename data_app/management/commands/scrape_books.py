
import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
from django.core.management import call_command
from django.core.management.base import BaseCommand
from data_app.models import Book
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import cohere
import time as time_lib
from decimal import Decimal, InvalidOperation
from data_project.settings import coherce_key

co = coherce_key

session = requests.Session()
api_calls_count = 0
max_api_calls = 100

def clean_data_with_cohere(data, original_data):
    global api_calls_count
    if api_calls_count >= max_api_calls:
        return data, False
    try:
        time_lib.sleep(0.5)
        # Sending the text data to Cohere for cleaning
        prompt = f"Clean the following data, remove any irrelevant or unwanted information:\n{data}"
        response = co.generate(
            model='command-xlarge',  # You can use other models like 'large', 'base', etc.
            prompt=prompt,
            max_tokens=150,
            stop_sequences=["\n"],
            temperature=0.7
        )
        cleaned_data = response.generations[0].text.strip()
        api_calls_count += 1
        print(f"API call #{api_calls_count} made.")
        is_cleaned = original_data != cleaned_data
        original_len = len(original_data)
        cleaned_len = len(cleaned_data)
        if original_len > 0:
            reduction_percentage = 100 * (original_len - cleaned_len) / original_len
            print(f"Data filtered by {reduction_percentage:.2f}%.")

        return cleaned_data, is_cleaned
    except Exception as e:
        print(f"Error cleaning data with Cohere: {str(e)}")
        time_lib.sleep(1)
        return data, False
def handle_price(price):
    try:
        cleaned_price = price.replace('£', '').strip()
        return Decimal(cleaned_price)
    except InvalidOperation:
        return Decimal('0.00')

class Command(BaseCommand):
    help = 'Scrapes data from Books to Scrape and stores it in the database and CSV file'

    def handle(self, *args, **kwargs):
        base_url = "https://books.toscrape.com/catalogue/page-{}.html"
        page = 1
        book_data = []  # List to store book data for CSV

        print("Starting to scrape...")

        while True:
            url = base_url.format(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the books on the page
            books = soup.find_all('article', class_='product_pod')

            if not books:
                break  # No more books, exit the loop

            for book in books:
                # Extract details of each book
                title = book.find('h3').find('a')['title']
                price = book.find('p', class_='price_color').text.strip()
                rating = book.find('p', class_='star-rating')['class'][1]
                availability = book.find('p', class_='instock availability').text.strip()

                # Handle category extraction
                category = 'Unknown'
                breadcrumb = soup.find('ul', class_='breadcrumb')
                if breadcrumb:
                    li_elements = breadcrumb.find_all('li')
                    if len(li_elements) > 2:
                        category = li_elements[2].text.strip()

                description = ''  # No description available on this page

                # Clean the data using Cohere (if applicable)
                cleaned_title, _ = clean_data_with_cohere(title, title)
                cleaned_price, _ = clean_data_with_cohere(price, price)
                cleaned_rating, _ = clean_data_with_cohere(rating, rating)
                cleaned_availability, _ = clean_data_with_cohere(availability, availability)
                cleaned_category, _ = clean_data_with_cohere(category, category)
                cleaned_description, _ = clean_data_with_cohere(description, description)

                # Handle price conversion (assuming it’s cleaned properly)
                valid_price = handle_price(cleaned_price)

                # Create and save the book, which will automatically encrypt the fields
                book_instance = Book(
                    title=cleaned_title,
                    price=str(valid_price),  # Price needs to be a string for encryption
                    rating=cleaned_rating,
                    availability=cleaned_availability,
                    category=cleaned_category,
                    description=cleaned_description
                )
                book_instance.save()  # Save the instance, which will trigger encryption

                # Append to CSV data (without encryption, as we're saving the encrypted data in DB)
                book_data.append({
                    'Title': cleaned_title,
                    'Price': str(valid_price),  # Store the plain value in the CSV
                    'Rating': cleaned_rating,
                    'Availability': cleaned_availability,
                    'Category': cleaned_category,
                    'Description': cleaned_description,
                })

            page += 1  # Go to the next page

        # Save the DataFrame to CSV
        df = pd.DataFrame(book_data)
        df.to_csv('books_to_scrape.csv', index=False)

        self.stdout.write(self.style.SUCCESS('Successfully scraped, cleaned, and saved books to the database and CSV!'))

@csrf_exempt
def scrape_and_import_books(request):
    try:
        call_command('scrape_books')  # Call the management command to scrape and save books
        return render(request, "success_page.html",
                      {"status": "success", "message": "Scraping and importing completed successfully!"})
    except Exception as e:
        return render(request, "error_page.html", {"status": "error", "message": str(e)})



from cryptography.fernet import Fernet
from django.core.management import call_command
from django.http import JsonResponse
import base64


def scrape_and_import_books(request):
    try:
        # Trigger the Django management command to scrape and import books
        call_command('scrape_books')  # This should match the file name, 'scrape_books.py'
        return JsonResponse({"status": "success", "message": "Scraping and importing completed successfully!"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
#
# key = Fernet.generate_key()
# print("this ia an encrypted key:",key)
#
# # Encrypt and Decrypt Functions
#
#
# def encrypt_data(data, key):
#     fernet = Fernet(key)
#     encrypted_data = fernet.encrypt(data.encode('utf-8'))
#     # Encode the encrypted data to base64 before returning
#     encrypted_data_base64 = base64.b64encode(encrypted_data).decode('utf-8')
#     return encrypted_data_base64
#
#
# def fix_base64_padding(base64_string):
#     # Ensure we are working with a string (not bytes) for base64 padding
#     if isinstance(base64_string, bytes):
#         base64_string = base64_string.decode('utf-8')
#
#     print(f"Original Base64 String: {base64_string}")
#     # Add padding if needed
#     padding_needed = 4 - (len(base64_string) % 4)
#     if padding_needed != 4:
#         base64_string += '=' * padding_needed
#
#     print(f"Padded Base64 String: {base64_string}")
#     return base64_string
#
# def decrypt_data(encrypted_data_base64, key):
#     fernet = Fernet(key)
#     try:
#         # Decode the base64 back to bytes before decrypting
#         encrypted_data = base64.b64decode(encrypted_data_base64)
#         decrypted_data = fernet.decrypt(encrypted_data).decode('utf-8')
#         return decrypted_data
#     except Exception as e:
#         print(f"Error during decryption: {e}")
#         return None

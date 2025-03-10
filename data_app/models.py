from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

# Generate a Fernet key and store it securely in settings.py
# Example: settings.ENCRYPTION_KEY = 'your_base64_32_bytes_key'
cipher_suite = Fernet(settings.ENCRYPTION_KEY)
# cipher_suite = encryption_key
print('this is cipher_suite:',cipher_suite)

class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=10)
    availability = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def encrypt_value(self, value):
        """Encrypt value before saving to the database."""
        if value is not None:
            return cipher_suite.encrypt(value.encode()).decode()  # Encrypt and return as string
        return value

    def decrypt_value(self, value):
        """Decrypt value when retrieving from the database."""
        if value is not None:
            try:
                # Decode the string to bytes before decrypting
                value_bytes = value.encode('utf-8')  # Ensure it's encoded to bytes
                decrypted_value = self.cipher_suite.decrypt(value_bytes).decode('utf-8')  # Decrypt and decode to string
                print(f"Decrypted Value: {decrypted_value}")
                return decrypted_value
            except Exception as e:
                # Optionally, log the error for debugging
                print(f"Error decrypting value: {e}")
                return value  # Return the raw value in case of an error
        return value

    def __str__(self):
        # Decrypt the title for display purposes
        return self.decrypt_value(self.title)

    def save(self, *args, **kwargs):
        # Encrypt the fields before saving to the database
        self.title = self.encrypt_value(self.title)
        self.price = self.encrypt_value(self.price)
        self.rating = self.encrypt_value(self.rating)
        self.availability = self.encrypt_value(self.availability)
        self.category = self.encrypt_value(self.category)
        self.description = self.encrypt_value(self.description)
        super().save(*args, **kwargs)

    # If you want to retrieve the decrypted values on object creation, you can use this method
    def get_decrypted_fields(self):
        return {
            'title': self.decrypt_value(self.title),
            'price': self.decrypt_value(self.price),
            'rating': self.decrypt_value(self.rating),
            'availability': self.decrypt_value(self.availability),
            'category': self.decrypt_value(self.category),
            'description': self.decrypt_value(self.description),
        }

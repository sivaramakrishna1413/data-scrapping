# from django.db import models
# # You can generate the key with Fernet.generate_key() and store it securely in settings
# from cryptography.fernet import Fernet
# from django.conf import settings
#
#
# # class EncryptedField(models.Field):
# #     def __init__(self, *args, **kwargs):
# #         # Make sure the key is being fetched correctly
# #         # self.secret_key = settings.SECRET_KEY  # This should be the correct Fernet key
# #         #
# #         # # Check if the secret_key is valid
# #         # try:
# #         #     self.cipher_suite = Fernet(self.secret_key)
# #         # except ValueError as e:
# #         #     raise ValueError(f"Invalid key in EncryptedField: {e}")
# #         #
# #         super().__init__(*args, **kwargs)
# #
# #     def get_prep_value(self, value):
# #         """Override to encrypt the value before storing in DB."""
# #         if value is not None:
# #             if isinstance(value, str):
# #                 value = self.cipher_suite.encrypt(value.encode()).decode()  # For string fields
# #             elif isinstance(value, float) or isinstance(value, int):
# #                 value = str(value)  # Convert numeric fields to string before encrypting
# #                 value = self.cipher_suite.encrypt(value.encode()).decode()  # Encrypt
# #         return value
# #
# #     def from_db_value(self, value, expression, connection):
# #         """Override to decrypt the value when retrieved from DB."""
# #         if value is not None:
# #             value = self.cipher_suite.decrypt(value.encode()).decode()
# #         return value
#
# class EncryptedDecimalField(models.DecimalField):
#     """For handling encrypted DecimalField."""
#     pass
#
# class EncryptedTextField(models.TextField):
#     """For handling encrypted TextField."""
#     pass
#
# class EncryptedCharField(models.CharField):
#     """For handling encrypted CharField."""
#     pass

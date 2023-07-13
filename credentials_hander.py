from cryptography.fernet import Fernet

with open("key.key", "rb") as key_file:
    key =  key_file.read()
with open("encrypted.key", "rb") as encrypted_message:
    encrypted_message =  encrypted_message.read()
    
fernet = Fernet(key)
decrypted_message = fernet.decrypt(encrypted_message)
OPENAI_API_KEY = decrypted_message.decode()
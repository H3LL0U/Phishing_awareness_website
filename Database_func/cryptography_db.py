import dotenv
from cryptography.fernet import Fernet
import base64
import hashlib

dotenv.load_dotenv()
config=dotenv.dotenv_values()
def convert_string_to_urlsafe_base64(string_to_encode:str):
    
    hash_value = hashlib.sha256(string_to_encode.encode()).digest()

    
    key = base64.urlsafe_b64encode(hash_value)

    
    return key



def encrypt_value(value:str,key=convert_string_to_urlsafe_base64(config["ENCRYPTION_KEY"])):

    """Encrypt a given value."""

    return Fernet(key).encrypt(value.encode()).decode()

def decrypt_value(value:str,key=convert_string_to_urlsafe_base64(config["ENCRYPTION_KEY"])):
    return Fernet(key).decrypt(value.encode()).decode()

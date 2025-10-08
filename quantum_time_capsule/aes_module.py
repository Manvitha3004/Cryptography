"""
AES Module for Quantum-Safe Digital Time Capsule

Handles symmetric encryption/decryption using AES via Fernet.
"""

from cryptography.fernet import Fernet
import base64


def generate_aes_key():
    """
    Generate a new AES key for Fernet.
    
    Returns:
        str: Base64 encoded AES key
    """
    return base64.urlsafe_b64encode(Fernet.generate_key()).decode()


def encrypt_message(message, aes_key_b64):
    """
    Encrypt a message using AES.
    
    Args:
        message (str): Plaintext message
        aes_key_b64 (str): Base64 encoded AES key
        
    Returns:
        str: Base64 encoded ciphertext
    """
    f = Fernet(aes_key_b64.encode())
    ciphertext = f.encrypt(message.encode())
    return base64.urlsafe_b64encode(ciphertext).decode()


def decrypt_message(ciphertext_b64, aes_key_b64):
    """
    Decrypt a message using AES.
    
    Args:
        ciphertext_b64 (str): Base64 encoded ciphertext
        aes_key_b64 (str): Base64 encoded AES key
        
    Returns:
        str: Decrypted plaintext
    """
    f = Fernet(aes_key_b64.encode())
    ciphertext = base64.urlsafe_b64decode(ciphertext_b64)
    plaintext = f.decrypt(ciphertext)
    return plaintext.decode()
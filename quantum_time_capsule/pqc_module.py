"""
PQC Module for Quantum-Safe Digital Time Capsule

Note: This implementation uses classical cryptography (RSA + ECDSA) for demonstration
since liboqs installation failed in this environment. For real PQC, use liboqs-python
with Kyber512 and Dilithium2.
"""

import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.backends import default_backend


def generate_keys():
    """
    Generate RSA key pair (simulating Kyber512) and ECDSA key pair (simulating Dilithium2).
    
    Returns:
        dict: Contains kem_public, kem_secret, sig_public, sig_secret as base64 strings
    """
    # Generate RSA keys for KEM simulation
    kem_private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    kem_public = kem_private.public_key()
    
    # Generate ECDSA keys for signature simulation
    sig_private = ec.generate_private_key(ec.SECP256R1(), default_backend())
    sig_public = sig_private.public_key()
    
    # Serialize to PEM then base64
    kem_private_pem = kem_private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    kem_public_pem = kem_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    sig_private_pem = sig_private.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    sig_public_pem = sig_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return {
        'kem_public': base64.b64encode(kem_public_pem).decode(),
        'kem_secret': base64.b64encode(kem_private_pem).decode(),
        'sig_public': base64.b64encode(sig_public_pem).decode(),
        'sig_secret': base64.b64encode(sig_private_pem).decode()
    }


def encapsulate_key(kem_public_b64):
    """
    Simulate KEM: Generate random AES key and "encapsulate" with RSA encryption.
    
    Args:
        kem_public_b64 (str): Base64 encoded RSA public key
        
    Returns:
        tuple: (ciphertext_b64, shared_secret_b64) - ciphertext is encrypted AES key, shared_secret is AES key
    """
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import os
    
    # Load public key
    kem_public_pem = base64.b64decode(kem_public_b64)
    kem_public = serialization.load_pem_public_key(kem_public_pem, backend=default_backend())
    
    # Generate random AES key (32 bytes)
    shared_secret = os.urandom(32)
    
    # Encrypt the AES key with RSA
    ciphertext = kem_public.encrypt(
        shared_secret,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return (
        base64.b64encode(ciphertext).decode(),
        base64.b64encode(shared_secret).decode()
    )


def decapsulate_key(kem_secret_b64, ciphertext_b64):
    """
    Simulate KEM decapsulation: Decrypt the AES key with RSA.
    
    Args:
        kem_secret_b64 (str): Base64 encoded RSA private key
        ciphertext_b64 (str): Base64 encoded encrypted AES key
        
    Returns:
        str: Base64 encoded AES key
    """
    # Load private key
    kem_secret_pem = base64.b64decode(kem_secret_b64)
    kem_secret = serialization.load_pem_private_key(kem_secret_pem, password=None, backend=default_backend())
    
    # Decrypt
    ciphertext = base64.b64decode(ciphertext_b64)
    shared_secret = kem_secret.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return base64.b64encode(shared_secret).decode()


def sign_data(data, sig_secret_b64):
    """
    Sign data using ECDSA (simulating Dilithium2).
    
    Args:
        data (str): Data to sign
        sig_secret_b64 (str): Base64 encoded ECDSA private key
        
    Returns:
        str: Base64 encoded signature
    """
    # Load private key
    sig_secret_pem = base64.b64decode(sig_secret_b64)
    sig_secret = serialization.load_pem_private_key(sig_secret_pem, password=None, backend=default_backend())
    
    # Sign
    signature = sig_secret.sign(
        data.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    
    return base64.b64encode(signature).decode()


def verify_signature(data, signature_b64, sig_public_b64):
    """
    Verify signature using ECDSA.
    
    Args:
        data (str): Original data
        signature_b64 (str): Base64 encoded signature
        sig_public_b64 (str): Base64 encoded ECDSA public key
        
    Returns:
        bool: True if signature is valid
    """
    # Load public key
    sig_public_pem = base64.b64decode(sig_public_b64)
    sig_public = serialization.load_pem_public_key(sig_public_pem, backend=default_backend())
    
    signature = base64.b64decode(signature_b64)
    
    try:
        sig_public.verify(signature, data.encode(), ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False
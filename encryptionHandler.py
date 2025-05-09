import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_token():
    return os.urandom(32)

def derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),    
        salt,
        100_000,
        dklen=32
    )

def encrypt_token(token: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padding_length = 16 - (len(token) % 16)
    padded_token = token + bytes([padding_length] * padding_length)

    return encryptor.update(padded_token) + encryptor.finalize()


def decrypt_token(encrypted: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    padded_token = decryptor.update(encrypted) + decryptor.finalize()

    padding_length = padded_token[-1]
    return padded_token[:-padding_length]

def createPassword(passwd):
    salt = os.urandom(16)
    iv = os.urandom(16)
    token = generate_token()

    key = derive_key(passwd, salt)
    encrypted_token = encrypt_token(token, key, iv)

    authentication = {
        "salt": salt,
        "iv": iv,
        "encrypted_token": encrypted_token
    }
    return authentication
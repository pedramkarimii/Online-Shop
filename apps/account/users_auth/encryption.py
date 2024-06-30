import base64
from typing import ByteString, Any

from Crypto.Cipher import AES
from Crypto.Cipher._mode_ecb import EcbMode
from Crypto.Util.Padding import pad, unpad


def get_new_cipher(key: ByteString) -> EcbMode:
    """
    Create a new AES cipher instance with ECB mode using the provided key.
    Args:
    - key (ByteString): The encryption key used to create the cipher.
    Returns:
    - EcbMode: AES ECB mode cipher instance.
    """
    return AES.new(key, AES.MODE_ECB)


def ciphertext_encrypt(cipher: EcbMode, data: str) -> ByteString:
    """
    Encrypt data using the provided AES ECB mode cipher.
    Args:
    - cipher (EcbMode): AES ECB mode cipher instance.
    - data (str): The data to encrypt in string format.
    Returns:
    - ByteString: Encrypted data in bytes format.
    """
    return cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))


def ciphertext_decode(encrypted_data: ByteString) -> bytes:
    """
    Decode base64 encoded encrypted data back to bytes.
    Args:
    - encrypted_data (ByteString): Base64 encoded encrypted data.
    Returns:
    - bytes: Decoded encrypted data in bytes format.
    Raises:
    - ValueError: If the input data is not valid base64 encoded.
    """
    try:
        cipher_decode = base64.b64decode(encrypted_data)
    except Exception as e:
        raise ValueError('Invalid encrypted data')
    else:
        return cipher_decode


def encrypt(data: str, key: ByteString) -> str:
    """
    Encrypt data using AES encryption with ECB mode and base64 encode the result.
    Args:
    - data (str): The data to encrypt in string format.
    - key (ByteString): The encryption key used for encryption.
    Returns:
    - str: Encrypted data in base64 encoded string format.
    """
    cipher = get_new_cipher(key=key)
    ciphertext = ciphertext_encrypt(cipher=cipher, data=data)
    encrypted = base64.b64encode(ciphertext).decode('utf-8')
    return encrypted


def decrypt(encrypted: ByteString, key: ByteString) -> str:
    """
    Decrypt base64 encoded encrypted data using AES decryption with ECB mode.
    Args:
    - encrypted (ByteString): Base64 encoded encrypted data to decrypt.
    - key (ByteString): The encryption key used for decryption.
    Returns:
    - str: Decrypted data in string format.
    Raises:
    - ValueError: If decryption fails due to incorrect padding or invalid data.
    """
    cipher = get_new_cipher(key=key)
    ciphertext = ciphertext_decode(encrypted_data=encrypted)
    try:
        decrypted_token = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    except Exception as e:
        raise ValueError(e)
    else:
        return decrypted_token

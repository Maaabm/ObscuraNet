# Module: chacha
# chacha.py

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os

class ChaCha20Encryptor:
    """
    A class that provides encryption and decryption using ChaCha20-Poly1305.
    It's fast, secure, and ideal for mobile or embedded environments.
    """

    def __init__(self, key: bytes = None):
        """
        Initialize the encryptor with a 32-byte symmetric key.
        If no key is provided, a random one is generated.
        """
        if key:
            if len(key) != 32:
                raise ValueError("ChaCha20-Poly1305 key must be exactly 32 bytes.")
            self.key = key
        else:
            self.key = ChaCha20Poly1305.generate_key()

        self.aead = ChaCha20Poly1305(self.key)  # AEAD = Authenticated Encryption with Associated Data

    def encrypt(self, plaintext: bytes, aad: bytes = b"") -> dict:
        """
        Encrypts the given plaintext using ChaCha20-Poly1305.

        Parameters:
        - plaintext: bytes to encrypt
        - aad: associated authenticated data (not encrypted but authenticated)

        Returns a dictionary containing:
        - ciphertext
        - nonce (needed for decryption)
        - aad (for reference)
        """
        nonce = os.urandom(12)  # 96-bit nonce as required by the algorithm
        ciphertext = self.aead.encrypt(nonce=nonce, data=plaintext, associated_data=aad)

        return {
            "ciphertext": ciphertext,
            "nonce": nonce,
            "aad": aad
        }

    def decrypt(self, ciphertext: bytes, nonce: bytes, aad: bytes = b"") -> bytes:
        """
        Decrypts the given ciphertext using ChaCha20-Poly1305.

        Parameters:
        - ciphertext: bytes to decrypt
        - nonce: must match the one used in encryption
        - aad: associated data used during encryption (must match exactly)

        Returns:
        - decrypted plaintext as bytes
        """
        return self.aead.decrypt(nonce=nonce, data=ciphertext, associated_data=aad)

    def get_key(self) -> bytes:
        """
        Returns the current symmetric key (useful for session sharing).
        """
        return self.key

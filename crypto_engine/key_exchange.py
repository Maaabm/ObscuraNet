# Module: key_exchange
# key_exchange.py

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

class Curve25519KeyExchange:
    """
    This class handles the generation of key pairs and the secure key exchange process
    using Curve25519 (based on Elliptic Curve Diffie-Hellman).
    """

    def __init__(self):
        """
        Generates a private/public key pair upon initialization.
        """
        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def get_public_bytes(self) -> bytes:
        """
        Returns the public key as bytes (used to send to peers).
        """
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

    def generate_shared_key(self, peer_public_bytes: bytes) -> bytes:
        """
        Given a peer's public key in bytes, calculates the shared secret.

        This shared secret is used as the symmetric session key 
        (can be passed into ChaCha20-Poly1305 or HKDF).

        Parameters:
        - peer_public_bytes: the raw byte-form of the peer’s Curve25519 public key

        Returns:
        - shared secret (bytes)
        """
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
        shared_key = self.private_key.exchange(peer_public_key)
        return shared_key

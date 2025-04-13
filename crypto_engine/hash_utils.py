# Module: hash_utils
# hash_utils.py

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend

def compute_sha3_256(data: bytes) -> str:
    """
    Computes a SHA3-256 hash of the input data.
    
    Parameters:
    - data: bytes to hash

    Returns:
    - Hexadecimal string of the hash
    """
    digest = hashes.Hash(hashes.SHA3_256(), backend=default_backend())
    digest.update(data)
    return digest.finalize().hex()

def derive_key_hkdf(shared_secret: bytes, salt: bytes = b"", info: bytes = b"ObscuraNet Session Key") -> bytes:
    """
    Derives a unique and secure key from a shared secret using HKDF.
    
    Parameters:
    - shared_secret: the raw shared key from ECDH
    - salt: optional random salt for better randomness (recommended)
    - info: context info (optional — helps derive different keys for different purposes)

    Returns:
    - A 32-byte key (suitable for ChaCha20-Poly1305)
    """
    hkdf = HKDF(
        algorithm=hashes.SHA3_256(),
        length=32,
        salt=salt,
        info=info,
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)

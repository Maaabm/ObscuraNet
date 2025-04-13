from crypto_engine.chacha import ChaCha20Encryptor
from crypto_engine.key_exchange import Curve25519KeyExchange
from crypto_engine.hash_utils import compute_sha3_256, derive_key_hkdf
from pow_system.adaptive_pow import AdaptivePoW
from pow_system.reputation_manager import ReputationManager

class SecureNode:
    """
    The SecureNode class represents a node in the ObscuraNet protocol.
    It handles secure messaging, encryption, ECDH key exchange,
    adaptive proof-of-work, and trust-based reputation scoring.
    """

    def __init__(self, node_id: str):
        """
        Initializes the node with a unique identifier.
        Generates Curve25519 key pair and initializes internal modules.
        """
        self.node_id = node_id                                # Unique identity for the node
        self.kex = Curve25519KeyExchange()                    # Key exchange system
        self.public_key = self.kex.get_public_bytes()         # Public key to share with peers
        self.shared_key = None                                # Session key derived from ECDH + HKDF
        self.encryptor = None                                 # Encryptor for secure messaging
        self.pow = AdaptivePoW()                              # Proof-of-work engine
        self.reputation = ReputationManager(node_id)          # Reputation tracking for trust
        self.peers = {}                                       # Stores known peers {peer_id: public_key}

    def get_public_key(self) -> bytes:
        """
        Returns this node’s public key to be shared with other peers.
        """
        return self.public_key

    def establish_session(self, peer_id: str, peer_public_key: bytes):
        """
        Establishes a secure session with a peer:
        - Stores the peer’s public key
        - Generates a shared ECDH secret
        - Derives a session key using HKDF
        - Initializes the ChaCha20 encryptor
        """
        self.peers[peer_id] = peer_public_key
        
        # Step 1: Perform ECDH key exchange
        raw_shared = self.kex.generate_shared_key(peer_public_key)

        # Step 2: Derive a uniform session key using HKDF (SHA3-256)
        self.shared_key = derive_key_hkdf(shared_secret=raw_shared)

        # Step 3: Use the derived key in our AEAD encryption engine
        self.encryptor = ChaCha20Encryptor(key=self.shared_key)

    def send_message(self, message: str, aad: bytes = b"") -> dict:
        """
        Encrypts a plaintext message using ChaCha20-Poly1305 and wraps it as a packet.
        Includes SHA3-256 hash for message integrity.

        Returns:
        - A dictionary representing a secure message packet
        """
        if not self.encryptor:
            raise Exception("Session not established. Cannot encrypt.")

        encrypted = self.encryptor.encrypt(plaintext=message.encode(), aad=aad)

        return {
            "from": self.node_id,
            "nonce": encrypted["nonce"],
            "aad": encrypted["aad"],
            "ciphertext": encrypted["ciphertext"],
            "hash": compute_sha3_256(encrypted["ciphertext"]),
        }

    def receive_message(self, packet: dict) -> str:
        """
        Decrypts a message packet and verifies its integrity.
        Raises an exception if tampering is detected.
        """
        if not self.encryptor:
            raise Exception("Session not established. Cannot decrypt.")

        # Verify integrity using SHA3-256
        expected_hash = compute_sha3_256(packet["ciphertext"])
        if expected_hash != packet["hash"]:
            raise Exception("Message integrity compromised! Hash mismatch.")

        # Decrypt and return plaintext
        decrypted = self.encryptor.decrypt(
            ciphertext=packet["ciphertext"],
            nonce=packet["nonce"],
            aad=packet["aad"]
        )

        return decrypted.decode()

    def get_status(self) -> dict:
        """
        Returns a dictionary of node status:
        - Reputation score
        - Current PoW difficulty
        - Connected peers
        """
        return {
            "node_id": self.node_id,
            "reputation": self.reputation.get_score(),
            "pow_difficulty": self.pow.get_current_difficulty(),
            "connected_peers": list(self.peers.keys())
        }

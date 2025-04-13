# Module: packet
import uuid
import time

class Packet:
    """
    Represents a network packet in the ObscuraNet protocol.
    A packet carries encrypted data along with metadata for routing, tracking, and analysis.
    """

    def __init__(self, sender_id: str, receiver_id: str, payload: bytes, is_dummy=False, mode="low-latency"):
        """
        Create a new packet.

        Parameters:
        - sender_id: ID of the sending node
        - receiver_id: ID of the intended next-hop or destination
        - payload: Encrypted message or dummy data (bytes)
        - is_dummy: Boolean indicating whether this is a dummy (decoy) packet
        - mode: Routing mode — e.g., "low-latency", "onion", "dtn"
        """
        self.packet_id = str(uuid.uuid4())       # Unique ID for tracking
        self.timestamp = int(time.time())         # Time packet was created
        self.sender_id = sender_id                # Who sent it
        self.receiver_id = receiver_id            # Who it's intended for
        self.payload = payload                    # Encrypted or dummy content
        self.is_dummy = is_dummy                  # True if this is a fake packet for obfuscation
        self.mode = mode                          # Routing mode

    def to_dict(self) -> dict:
        """
        Convert packet to dictionary format for sending or logging.

        Returns:
        - Dictionary with all packet fields.
        """
        return {
            "packet_id": self.packet_id,
            "timestamp": self.timestamp,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "payload": self.payload,
            "is_dummy": self.is_dummy,
            "mode": self.mode
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Reconstruct a Packet object from a dictionary (e.g., after network deserialization).

        Parameters:
        - data: Dictionary containing all expected packet fields

        Returns:
        - Reconstructed Packet instance
        """
        pkt = Packet(
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            payload=data["payload"],
            is_dummy=data.get("is_dummy", False),
            mode=data.get("mode", "low-latency")
        )
        pkt.packet_id = data.get("packet_id", str(uuid.uuid4()))
        pkt.timestamp = data.get("timestamp", int(time.time()))
        return pkt

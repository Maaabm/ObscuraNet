# Module: low_latency
# low_latency.py

from core.packet import Packet
from core.secure_node import SecureNode

class LowLatencyRouter:
    """
    Handles low-latency direct routing for small, low-risk messages.
    Uses ChaCha20 encryption and sends directly to the peer with no intermediate hops.
    """

    def __init__(self, node: SecureNode):
        """
        Initialize with a reference to the current secure node.
        """
        self.node = node

    def send(self, receiver_id: str, message: str) -> Packet:
        """
        Encrypts and wraps a message into a low-latency packet.
        Returns a Packet object to be sent directly to receiver.
        """
        if len(message.encode()) > 512:
            raise ValueError("Low-latency mode supports only messages <= 512 bytes.")

        if receiver_id not in self.node.peers:
            raise Exception("Receiver public key not found. Establish session first.")

        # Encrypt message using secure node’s ChaCha20 session
        packet_data = self.node.send_message(message, aad=b"low-latency")

        # Wrap in a Packet
        packet = Packet(
            sender_id=self.node.node_id,
            receiver_id=receiver_id,
            payload=packet_data["ciphertext"],
            is_dummy=False,
            mode="low-latency"
        )

        return packet

    def receive(self, packet: Packet) -> str:
        """
        Decrypts and returns the message content from a low-latency packet.
        """
        if packet.mode != "low-latency":
            raise Exception("Packet mode mismatch. Expected low-latency.")

        # Rebuild packet into dictionary form expected by SecureNode
        packet_dict = {
            "from": packet.sender_id,
            "nonce": b"",  # Needs to be tracked/stored in real transmission
            "aad": b"low-latency",
            "ciphertext": packet.payload,
            "hash": ""
        }

        # This is a placeholder — in practice, you'll transmit nonce + hash too
        return self.node.receive_message(packet_dict)

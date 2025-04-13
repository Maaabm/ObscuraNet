# Module: opportunistic_dtn
# opportunistic_dtn.py

from core.packet import Packet
from core.secure_node import SecureNode
import math
import random

class DTNRouter:
    """
    Delay-Tolerant Networking (DTN) Router for large file transfers.
    Splits data into fragments and mixes with dummy packets for traffic obfuscation.
    """

    def __init__(self, node: SecureNode):
        self.node = node

    def fragment_message(self, message: bytes, fragment_size: int = 256) -> list:
        """
        Splits a large message into fixed-size fragments.
        """
        return [message[i:i + fragment_size] for i in range(0, len(message), fragment_size)]

    def send_bulk(self, receiver_id: str, message: str, dummy_ratio: float = 0.3) -> list:
        """
        Sends a bulk message by splitting into encrypted packets with dummy traffic.

        Parameters:
        - receiver_id: Destination node
        - message: The large string message
        - dummy_ratio: Percentage of dummy packets to add (0.3 = 30%)

        Returns:
        - List of Packet instances (real + dummy, shuffled)
        """
        aad = b"dtn-mode"
        message_bytes = message.encode()
        fragments = self.fragment_message(message_bytes)
        packets = []

        # Create real packets
        for fragment in fragments:
            encrypted = self.node.send_message(fragment.decode('latin1'), aad=aad)
            packet = Packet(
                sender_id=self.node.node_id,
                receiver_id=receiver_id,
                payload=encrypted["ciphertext"],
                is_dummy=False,
                mode="dtn"
            )
            packets.append(packet)

        # Create dummy packets
        num_dummies = math.ceil(len(packets) * dummy_ratio)
        for _ in range(num_dummies):
            dummy_data = b"0" * random.randint(128, 256)
            packet = Packet(
                sender_id=self.node.node_id,
                receiver_id=receiver_id,
                payload=dummy_data,
                is_dummy=True,
                mode="dtn"
            )
            packets.append(packet)

        random.shuffle(packets)  # Obfuscate order
        return packets

    def receive_bulk(self, packets: list) -> str:
        """
        Reassembles the original message by filtering real packets and decrypting them.

        Parameters:
        - packets: List of Packet instances

        Returns:
        - Reconstructed full message (str)
        """
        real_fragments = []
        for pkt in packets:
            if pkt.is_dummy:
                continue

            # Simulate minimal metadata packet
            pkt_dict = {
                "from": pkt.sender_id,
                "nonce": b"",       # Placeholder — should be sent with packet
                "aad": b"dtn-mode",
                "ciphertext": pkt.payload,
                "hash": ""
            }

            try:
                part = self.node.receive_message(pkt_dict)
                real_fragments.append(part)
            except Exception as e:
                continue  # Drop failed fragments

        return ''.join(real_fragments)

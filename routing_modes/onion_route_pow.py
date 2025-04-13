# Module: onion_route_pow
# onion_route_pow.py

import random
from core.packet import Packet
from core.secure_node import SecureNode

class OnionRouter:
    """
    Implements multi-hop onion routing with adaptive proof-of-work.
    Used for high-security messages (authentication, critical data).
    """

    def __init__(self, node: SecureNode, network_map: dict):
        """
        node: SecureNode instance (this node)
        network_map: {node_id: SecureNode instance} for simulated multi-hop routing
        """
        self.node = node
        self.network_map = network_map

    def create_onion_message(self, path: list, final_message: str) -> Packet:
        """
        Constructs a layered packet where each node only sees the next hop and one layer of encryption.

        path: ordered list of node_ids (including destination at the end)
        final_message: actual message to be delivered at the end
        """
        message = final_message.encode()
        aad = b"onion-route"

        for peer_id in reversed(path[1:]):  # Exclude sender (self)
            # Establish session with each peer (if not done already)
            peer_public_key = self.network_map[peer_id].get_public_key()
            self.node.establish_session(peer_id, peer_public_key)

            # Encrypt the current message layer with that peer's key
            layer = self.node.send_message(message.decode(), aad=aad)
            message = layer["ciphertext"]  # Each layer becomes the new inner payload

        # Final payload is encrypted for first hop
        return Packet(
            sender_id=self.node.node_id,
            receiver_id=path[1],
            payload=message,
            is_dummy=False,
            mode="onion"
        )

    def process_packet(self, packet: Packet, path: list) -> str:
        """
        Simulate processing a packet through each node in the path.
        Each hop decrypts one layer and passes it to the next.
        """
        current_payload = packet.payload
        aad = b"onion-route"

        for hop in path[1:]:
            # Each node decrypts its layer
            self.node.establish_session(hop, self.network_map[hop].get_public_key())
            encrypted_layer = {
                "from": self.node.node_id,
                "nonce": b"",  # In a real network, these must be passed
                "aad": aad,
                "ciphertext": current_payload,
                "hash": ""     # For testing only
            }

            try:
                # Solve PoW before processing (skip if trusted)
                if not self.node.pow.is_trusted(hop):
                    puzzle = self.node.pow.generate_puzzle("forward packet")
                    solution, _ = self.node.pow.solve_puzzle(
                        puzzle["message"],
                        puzzle["nonce_seed"],
                        puzzle["difficulty"]
                    )
                    assert self.node.pow.verify_solution(
                        puzzle["message"],
                        puzzle["nonce_seed"],
                        solution,
                        puzzle["difficulty"]
                    )

                # Decrypt this layer
                decrypted = self.node.receive_message(encrypted_layer)
                current_payload = decrypted.encode()  # Prepare for next hop
            except Exception as e:
                return f"Error during hop '{hop}': {e}"

        return decrypted

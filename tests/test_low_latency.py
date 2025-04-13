from core.secure_node import SecureNode
from routing_modes.low_latency import LowLatencyRouter

# Step 1: Create two secure nodes (simulating two devices in the network)
node_a = SecureNode("NodeA")
node_b = SecureNode("NodeB")

# Step 2: Exchange public keys and establish a secure session
node_a.establish_session("NodeB", node_b.get_public_key())
node_b.establish_session("NodeA", node_a.get_public_key())

# Step 3: Each node gets a LowLatencyRouter instance
router_a = LowLatencyRouter(node_a)
router_b = LowLatencyRouter(node_b)

# Step 4: Node A sends a short message to Node B
message = "Hello from Node A via Low-Latency Mode"
packet = router_a.send("NodeB", message)

# NOTE: The 'send' method only packs encrypted payload. We now simulate full packet structure
# including nonce, aad, and hash to be passed to the receiving node.

# Use the secure node's encryption output to create a simulated message dict
# This is normally handled in real routing layers or over-the-wire protocol
packet_data = node_a.send_message(message, aad=b"low-latency")

# Combine all needed info into one dictionary as expected by receive_message()
incoming_packet_dict = {
    "from": packet.sender_id,
    "nonce": packet_data["nonce"],
    "aad": packet_data["aad"],
    "ciphertext": packet_data["ciphertext"],
    "hash": packet_data["hash"]
}

# Step 5: Node B receives and decrypts the message
received_message = node_b.receive_message(incoming_packet_dict)

# Step 6: Output the result
print("Original Message Sent:", message)
print("Decrypted Message Received:", received_message)

from core.secure_node import SecureNode
from routing_modes.onion_route_pow import OnionRouter

# Step 1: Create 3 secure nodes to simulate a multi-hop onion path
node_a = SecureNode("NodeA")
node_b = SecureNode("NodeB")
node_c = SecureNode("NodeC")

# Step 2: Simulate the network map (ID to SecureNode instance)
network = {
    "NodeA": node_a,
    "NodeB": node_b,
    "NodeC": node_c
}

# Step 3: Create OnionRouter for Node A (the sender)
router = OnionRouter(node=node_a, network_map=network)

# Step 4: Define routing path from NodeA -> NodeB -> NodeC (destination)
path = ["NodeA", "NodeB", "NodeC"]

# Step 5: Message to be securely sent
message = "This is a secure message using onion routing!"

# Step 6: Create the onion-encrypted packet
packet = router.create_onion_message(path, message)

# Step 7: Simulate routing the packet through each hop
final_result = router.process_packet(packet, path)

# Step 8: Output the final decrypted message
print("Original Message:", message)
print("Final Decrypted Message:", final_result)

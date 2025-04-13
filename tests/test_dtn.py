from core.secure_node import SecureNode
from routing_modes.opportunistic_dtn import DTNRouter

# Step 1: Create two secure nodes (sender and receiver)
sender = SecureNode("SenderNode")
receiver = SecureNode("ReceiverNode")

# Step 2: Exchange public keys and establish secure session
sender.establish_session("ReceiverNode", receiver.get_public_key())
receiver.establish_session("SenderNode", sender.get_public_key())

# Step 3: Create DTNRouter for sender
router = DTNRouter(sender)

# Step 4: Prepare a large message to simulate file-like data
large_message = "This is a very large file or message. " * 20  # ~1000+ bytes

# Step 5: Send the message using DTN (with 30% dummy packets)
packets = router.send_bulk("ReceiverNode", large_message, dummy_ratio=0.3)

# Display count of packets sent
print(f"Total packets sent (including dummy): {len(packets)}")
print(f"Dummy packets: {len([p for p in packets if p.is_dummy])}")

# Step 6: Reassemble the message at receiver
receiver_router = DTNRouter(receiver)
reconstructed = receiver_router.receive_bulk(packets)

# Step 7: Compare results
print("\nOriginal Message Start:", large_message[:100], "...")
print("Reconstructed Message Start:", reconstructed[:100], "...")
print("✅ Match:", reconstructed == large_message)

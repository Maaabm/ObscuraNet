from core.packet import Packet

# Step 1: Create a real data packet
real_packet = Packet(
    sender_id="NodeA",
    receiver_id="NodeB",
    payload=b"This is a secure payload.",
    is_dummy=False,
    mode="low-latency"
)

# Convert to dictionary
packet_dict = real_packet.to_dict()
print("Packet as dictionary:", packet_dict)

# Step 2: Reconstruct the packet from dict
reconstructed = Packet.from_dict(packet_dict)
print("Reconstructed Packet ID:", reconstructed.packet_id)
print("Reconstructed Sender:", reconstructed.sender_id)
print("Reconstructed Payload:", reconstructed.payload.decode())
print("Is Dummy?", reconstructed.is_dummy)
print("Routing Mode:", reconstructed.mode)

# Step 3: Create a dummy packet
dummy_packet = Packet(
    sender_id="NodeX",
    receiver_id="NodeY",
    payload=b"XXXXX",
    is_dummy=True,
    mode="low-latency"
)

print("Dummy Packet:", dummy_packet.to_dict())

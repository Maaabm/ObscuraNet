from pow_system.reputation_manager import ReputationManager

# Step 1: Create a reputation manager for a test node
rep = ReputationManager("node123")

# Step 2: Show initial reputation score
print("Initial Score:", rep.get_score())

# Step 3: Simulate 5 successful relays
for _ in range(5):
    rep.increment_success()
print("Score after 5 successes:", rep.get_score())

# Step 4: Simulate 3 failed relays
for _ in range(3):
    rep.increment_failure()
print("Score after 3 failures:", rep.get_score())

# Step 5: Check trust level
print("Is Trusted?", rep.is_trusted())    # Should be True if score >= 120
print("Is Flagged?", rep.is_flagged())    # Should be False unless score <= 40

# Step 6: Simulate more failures to drop reputation
for _ in range(15):
    rep.increment_failure()
print("Score after more failures:", rep.get_score())
print("Is Flagged Now?", rep.is_flagged())

# Step 7: Reset everything
rep.reset()
print("After Reset:", rep.get_score())
print("Is Trusted After Reset?", rep.is_trusted())
print("Is Flagged After Reset?", rep.is_flagged())

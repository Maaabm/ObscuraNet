# Module: reputation_manager
# reputation_manager.py

class ReputationManager:
    """
    Tracks and manages the reputation of a node.
    Reputation is used to determine whether a node can bypass PoW or is flagged as untrustworthy.
    """

    def __init__(self, node_id: str):
        """
        Initialize the manager with default scores.
        """
        self.node_id = node_id
        self.score = 100  # Reputation starts at 100 by default
        self.successful_relay_count = 0
        self.failed_relay_count = 0

    def get_score(self) -> int:
        """
        Returns the current reputation score.
        """
        return self.score

    def increment_success(self):
        """
        Call this when a relay or action completes successfully.
        Increases the score slightly.
        """
        self.successful_relay_count += 1
        self.score = min(150, self.score + 2)

    def increment_failure(self):
        """
        Call this when a node fails to relay or drops packets.
        Decreases the score more significantly.
        """
        self.failed_relay_count += 1
        self.score = max(0, self.score - 5)

    def is_trusted(self) -> bool:
        """
        Returns True if the node is trusted enough to skip PoW.
        Threshold is score >= 120.
        """
        return self.score >= 120

    def is_flagged(self) -> bool:
        """
        Returns True if the node is flagged as unreliable.
        Threshold is score <= 40.
        """
        return self.score <= 40

    def reset(self):
        """
        Resets reputation and counters to default.
        Useful for testing or rejoining the network.
        """
        self.score = 100
        self.successful_relay_count = 0
        self.failed_relay_count = 0

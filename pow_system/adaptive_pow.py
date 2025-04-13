# Module: adaptive_pow
# adaptive_pow.py

import hashlib
import time
import random

class AdaptivePoW:
    """
    Adaptive Proof-of-Work (PoW) system.
    Protects against spam/Sybil attacks by requiring lightweight computational puzzles.
    Dynamically adjusts difficulty based on system state or attack detection.
    """

    def __init__(self, initial_difficulty=4):
        """
        Initialize PoW with a default starting difficulty.
        Higher difficulty = more leading zeros required in hash.
        """
        self.current_difficulty = initial_difficulty  # Number of leading zeros required
        self.trusted_nodes = set()  # Node IDs that can bypass PoW

    def get_current_difficulty(self) -> int:
        """
        Return the current difficulty level.
        """
        return self.current_difficulty

    def adjust_difficulty(self, under_attack: bool, network_congested: bool):
        """
        Adjust PoW difficulty based on network state.
        """
        if under_attack:
            self.current_difficulty = min(self.current_difficulty + 2, 10)
        elif network_congested:
            self.current_difficulty = min(self.current_difficulty + 1, 8)
        else:
            self.current_difficulty = max(self.current_difficulty - 1, 2)

    def is_trusted(self, node_id: str) -> bool:
        """
        Check if a node is marked as trusted (bypasses PoW).
        """
        return node_id in self.trusted_nodes

    def mark_as_trusted(self, node_id: str):
        """
        Add a node to the trusted list (PoW bypass).
        """
        self.trusted_nodes.add(node_id)

    def generate_puzzle(self, message: str, nonce_length: int = 8) -> dict:
        """
        Generate a PoW puzzle.
        Return a message and a random nonce to start solving.
        """
        nonce = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=nonce_length))
        return {
            "message": message,
            "nonce_seed": nonce,
            "difficulty": self.current_difficulty
        }

    def solve_puzzle(self, message: str, nonce_seed: str, difficulty: int) -> tuple:
        """
        Brute-force solution: find a nonce such that
        SHA3_256(message + nonce_seed + nonce) starts with `difficulty` zeros.
        Returns: (valid_nonce, time_taken)
        """
        prefix = "0" * difficulty
        nonce = 0
        start_time = time.time()

        while True:
            test_input = f"{message}{nonce_seed}{nonce}".encode()
            hash_result = hashlib.sha3_256(test_input).hexdigest()
            if hash_result.startswith(prefix):
                break
            nonce += 1

        return str(nonce), round(time.time() - start_time, 3)

    def verify_solution(self, message: str, nonce_seed: str, nonce: str, difficulty: int) -> bool:
        """
        Verify that a given solution is valid for the puzzle.
        """
        test_input = f"{message}{nonce_seed}{nonce}".encode()
        hash_result = hashlib.sha3_256(test_input).hexdigest()
        return hash_result.startswith("0" * difficulty)

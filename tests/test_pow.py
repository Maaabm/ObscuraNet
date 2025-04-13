from pow_system.adaptive_pow import AdaptivePoW

pow = AdaptivePoW()
puzzle = pow.generate_puzzle("relay this message")
print("Puzzle:", puzzle)

solution, time_taken = pow.solve_puzzle(puzzle["message"], puzzle["nonce_seed"], puzzle["difficulty"])
print("Solved with nonce:", solution, "in", time_taken, "seconds")

is_valid = pow.verify_solution(puzzle["message"], puzzle["nonce_seed"], solution, puzzle["difficulty"])
print("Valid:", is_valid)

r"""
Sparse-ruler impartial game solver (no uniqueness constraint on differences)

Rules assumed (normal-play):
- Universe U is a set of integer marks provided by the user (e.g., 0,1,2,3).
- A position is a subset S ⊆ U of marks already chosen.
- A legal move adds any unused mark x ∈ U−S. We do NOT require pairwise
    differences to be unique.
- Terminal positions are those with NO legal moves (i.e., S = U); the player
    who made the last move wins, so terminal positions are P-positions.

N/P classification:
- N-position: at least one legal move to a P-position.
- P-position: no legal moves OR all legal moves go to N-positions.

This script asks for an input sequence (e.g., "0123" or "0,1,2,3") and prints
the N/P status of the start position (empty set) and, for small sizes, the
classification of all reachable game states grouped by size.
"""

from collections import defaultdict
from functools import lru_cache
from itertools import combinations


def parse_sequence(s: str) -> list[int]:
    s = s.strip()
    if not s:
        return []
    # Accept formats: "01234", "0 1 2 3", "0,1,2,3"
    if all(ch.isdigit() for ch in s):
        return sorted({int(ch) for ch in s})
    # Replace separators with spaces
    for sep in ",;|/":
        s = s.replace(sep, " ")
    parts = [p for p in s.split() if p]
    return sorted({int(p) for p in parts})


def is_sparse(_marks: tuple[int, ...]) -> bool:
    # Unused now (kept for compatibility). Always True since we removed the
    # uniqueness constraint.
    return True


def legal_moves(universe: tuple[int, ...], state: tuple[int, ...]) -> list[int]:
    u_set = set(universe)
    s_set = set(state)
    moves = []
    for x in u_set - s_set:
        # No constraint: any unused mark is legal
        moves.append(x)
    return sorted(moves)


def classify_all_states(universe: list[int]):
    U = tuple(sorted(universe))

    @lru_cache(maxsize=None)
    def classify(state: tuple[int, ...]) -> str:
        moves = legal_moves(U, state)

        ####fix this logic to match new rule of the sparse ruler game 
        
        if not moves:
            return "P"  # terminal
        # N if any move to P
        for x in moves:
            nxt = tuple(sorted((*state, x)))
            if classify(nxt) == "P":
                return "N"
        return "P"

    # Build labels for all reachable states from empty
    labels: dict[tuple[int, ...], str] = {}

    def dfs(state: tuple[int, ...]):
        if state in labels:
            return
        labels[state] = classify(state)
        for x in legal_moves(U, state):
            dfs(tuple(sorted((*state, x))))

    dfs(())
    return labels


def format_state(state: tuple[int, ...]) -> str:
    return "".join(str(x) for x in state) if state else "∅"


def show_summary(universe: list[int], labels: dict[tuple[int, ...], str]):
    start = ()
    start_label = labels[start]
    print(f"Universe: {''.join(str(x) for x in universe)}")
    print(f"Start (empty set) is: {start_label}")
    # Group by size for a compact view (similar to whiteboard layers)
    by_size = defaultdict(list)
    for state, lab in labels.items():
        by_size[len(state)].append((state, lab))
    for k in sorted(by_size):
        layer = " ".join(f"{format_state(s)}{lab}" for s, lab in sorted(by_size[k]))
        print(f"size {k}: {layer}")


def main():
    seq = input("Enter sequence (e.g., 01234 or 0,1,2,3): ").strip()
    universe = parse_sequence(seq)
    if not universe:
        print("No marks provided.")
        return
    labels = classify_all_states(universe)
    show_summary(universe, labels)


if __name__ == "__main__":
    main()

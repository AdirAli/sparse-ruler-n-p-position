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


def is_sparse_ruler(state: tuple[int, ...], universe: tuple[int, ...]) -> bool:
    """Return True when `state` is a (sparse) ruler for the given universe.

    Definition used here: the set of positive pairwise differences of marks
    in `state` covers every integer distance from 1 up to the full span of the
    universe (max(universe)-min(universe)). In that case the marks can
    represent any distance in the universe and we'll treat that state as a
    P-position (terminal-like) per the requested rule.

    Example: universe=(0,1,2,3,4), state=(0,1,2,4) has differences {1,2,3,4}
    which covers 1..4 so it's a sparse ruler.
    """
    if not state:
        return False
    if not universe:
        return False
    span = max(universe) - min(universe)
    if span <= 0:
        return False
    # compute positive differences between marks in the state
    diffs = set()
    for a, b in combinations(state, 2):
        diffs.add(abs(a - b))
    # need to cover all distances 1..span
    needed = set(range(1, span + 1))
    return needed.issubset(diffs)


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
        # If the current state already forms a sparse ruler for the universe,
        # treat it as a P-position (player who moved to this state can be
        # considered to have completed the ruler).
        if is_sparse_ruler(state, U):
            return "P"

        if not_moves := (not moves):
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


def export_mermaid(labels: dict[tuple[int, ...], str], universe: list[int], out_path: str) -> None:
    """Export the decision tree as a Mermaid `graph TD` diagram.

    Each state becomes a node with a short label (state string and N/P). Edges
    represent legal moves. The generated `.mmd` file can be previewed in
    editors that support Mermaid or converted to SVG with mermaid-cli.
    """
    # Assign simple unique ids to nodes (n0, n1, ...)
    nodes = list(labels.keys())
    id_map = {state: f"n{i}" for i, state in enumerate(nodes)}

    def node_label(state: tuple[int, ...]) -> str:
        lab = labels[state]
        name = format_state(state)
        # Escape quotes and newlines for Mermaid
        text = name + "\\n" + lab
        return text.replace('"', "'")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("graph TD\n")
        # Nodes
        for state in nodes:
            nid = id_map[state]
            lbl = node_label(state)
            # Use Mermaid quoted label syntax: n0["label"]
            f.write(f"    {nid}[\"{lbl}\"]\n")
        f.write("\n")
        # Edges
        U = tuple(sorted(universe))
        for state in nodes:
            src = id_map[state]
            for x in legal_moves(U, state):
                nxt = tuple(sorted((*state, x)))
                if nxt in id_map:
                    dst = id_map[nxt]
                    f.write(f"    {src} --> {dst}\n")

    print(f"Wrote Mermaid file: {out_path}")


def main():
    seq = input("Enter sequence (e.g., 01234 or 0,1,2,3): ").strip()
    universe = parse_sequence(seq)
    if not universe:
        print("No marks provided.")
        return
    labels = classify_all_states(universe)
    show_summary(universe, labels)
    # Export a Mermaid file for visualization
    # sanitize sequence string for filename
    seq_name = "".join(str(x) for x in universe)
    out_fn = f"decision_tree_{seq_name}.mmd"
    try:
        export_mermaid(labels, universe, out_fn)
    except Exception as e:
        print(f"Failed to write Mermaid file: {e}")


if __name__ == "__main__":
    main()

"""Compute Grundy (nimber) sequence for the Kayles (Kayle) game.

Rules implemented (standard Kayles):
- A pile is a row of n adjacent pins.
- A move is either remove one pin, or remove two adjacent pins.
- Removing pins may split the pile into two independent piles.

This module computes Grundy numbers for pile sizes 0..N using recursion+memo.
"""
from typing import List, Dict

def mex(s: set) -> int:
    """Minimum excludant of a set of non-negative integers."""
    i = 0
    while True:
        if i not in s:
            return i
        i += 1


def grundy(n: int, memo: Dict[int, int] | None = None) -> int:
    """Return Grundy number for a single Kayles pile of size `n`.

    Uses memoization; move options:
    - remove single pin at position i -> splits into (i, n-i-1)
    - remove two adjacent pins at positions (i, i+1) -> splits into (i, n-i-2)
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 0:
        memo[n] = 0
        return 0

    reachable = set()
    # remove one pin
    for i in range(n):
        left = i
        right = n - i - 1
        g = grundy(left, memo) ^ grundy(right, memo)
        reachable.add(g)

    # remove two adjacent pins
    for i in range(n - 1):
        left = i
        right = n - i - 2
        g = grundy(left, memo) ^ grundy(right, memo)
        reachable.add(g)

    g_n = mex(reachable)
    memo[n] = g_n
    return g_n


def grundy_sequence(N: int) -> List[int]:
    """Return list of Grundy numbers for pile sizes 0..N."""
    memo: Dict[int, int] = {0: 0}
    seq = []
    for i in range(N + 1):
        seq.append(grundy(i, memo))
    return seq


if __name__ == "__main__":
    # quick smoke run
    print(grundy_sequence(20))

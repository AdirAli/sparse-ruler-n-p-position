"""Bitmask DP solver for the sparse-ruler Grundy computation.

Usage:
  python3 scripts/grundy_bitmask.py N

Computes the Grundy (start position) for universe marks 0..N.
This implementation uses integer masks and an efficient sparse-ruler
check based on bit shifts: difference d exists in mask m iff m & (m >> d)
has a 1-bit.
"""
from __future__ import annotations
import time
import sys


def is_sparse_ruler_mask(mask: int, n: int) -> bool:
    """Return True when `mask` (marks 0..n) already covers differences 1..n.

    We compute differences present by checking for each d in 1..n if
    `mask & (mask >> d)` is non-zero (meaning there exists a pair of bits
    at distance d). We build a bitmask of differences and compare against
    the needed mask `(1<<n)-1`.
    """
    if mask == 0:
        return False
    span = n
    needed = (1 << span) - 1 if span > 0 else 0
    diffs = 0
    for d in range(1, span + 1):
        if mask & (mask >> d):
            diffs |= 1 << (d - 1)
    return diffs == needed


def compute_start_grundy_bitmask(n: int) -> int:
    """Compute Grundy number for empty set for universe 0..n using DP.

    Returns the Grundy of mask 0.
    """
    m_count = n + 1
    full = (1 << m_count) - 1
    G = [0] * (full + 1)

    for m in range(full, -1, -1):
        if m == full or is_sparse_ruler_mask(m, n):
            G[m] = 0
            continue

        seen = bytearray(m_count + 3)  
        missing = (~m) & full
        b = missing
        while b:
            lsb = b & -b
            i = (lsb.bit_length() - 1)
            succ = m | (1 << i)
            g = G[succ]
            if g < len(seen):
                seen[g] = 1
            b -= lsb

        # mex
        mex = 0
        while mex < len(seen) and seen[mex]:
            mex += 1
        G[m] = mex

    return G[0]


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: grundy_bitmask.py N", file=sys.stderr)
        raise SystemExit(2)
    n = int(argv[0])
    t0 = time.time()
    g = compute_start_grundy_bitmask(n)
    t1 = time.time()
    print(f"start_grundy({n}) = {g}  (time {t1-t0:.3f}s)")


if __name__ == "__main__":
    main()

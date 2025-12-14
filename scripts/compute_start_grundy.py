"""Compute `start_grundy` for a universe 0..s and print the value.

This helper is designed to be launched as a subprocess so the caller can
apply a timeout per-size to avoid long hangs.
"""
import sys
from pathlib import Path
import importlib.util


def load_solver_module(path):
    spec = importlib.util.spec_from_file_location("sparse_solver", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    if len(sys.argv) < 2:
        print("Usage: compute_start_grundy.py SIZE", file=sys.stderr)
        raise SystemExit(2)
    s = int(sys.argv[1])
    repo_root = Path(__file__).resolve().parents[1]
    solver_path = repo_root / "sparse.n.p-position.py"
    solver = load_solver_module(solver_path)
    universe = list(range(s + 1))
    g = solver.start_grundy(universe)
    print(g)


if __name__ == "__main__":
    main()

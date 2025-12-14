"""Generate `universe_grundy.txt` with two columns: size and start_grundy.

This script uses the solver in `sparse.n.p-position.py`.
By default it computes sizes 0..20. You may pass optional positional
arguments: `start end` to compute an arbitrary inclusive range.
Example: `python3 scripts/generate_universe_grundy.py 21 100`.
"""
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import importlib.util


def load_solver_module(path):
    spec = importlib.util.spec_from_file_location("sparse_solver", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    out_path = REPO_ROOT / "universe_grundy.txt"
    solver_path = REPO_ROOT / "sparse.n.p-position.py"
    solver = load_solver_module(solver_path)

    import argparse

    p = argparse.ArgumentParser(description="Generate universe_grundy.txt for a range of sizes")
    p.add_argument("start", nargs="?", type=int, default=0, help="starting size (inclusive)")
    p.add_argument("end", nargs="?", type=int, default=20, help="ending size (inclusive)")
    p.add_argument("--timeout", "-t", type=int, default=30, help="per-size timeout in seconds (default 30)")
    args = p.parse_args()

    s0 = args.start
    s1 = args.end
    if s0 < 0 or s1 < s0:
        raise SystemExit("Invalid range")

    p_timeout = args.timeout
    import subprocess

    lines = []
    lines.append("size\tstart_grundy\n")
    for s in range(s0, s1 + 1):
        print(f"Computing size {s} (timeout {p_timeout}s)...", flush=True)
        try:
            
            proc = subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts" / "compute_start_grundy.py"), str(s)],
                capture_output=True,
                text=True,
                timeout=p_timeout,
            )
            if proc.returncode == 0:
                g = proc.stdout.strip()
            else:
                g = f"ERR({proc.returncode})"
        except subprocess.TimeoutExpired:
            g = "TIMEOUT"
        lines.append(f"{s}\t{g}\n")
    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out_path} with sizes {s0}..{s1}")


if __name__ == "__main__":
    main()

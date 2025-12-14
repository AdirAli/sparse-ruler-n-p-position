"""CLI to compute and print Kayles (Kayle) Grundy numbers for pile sizes 0..N."""
import argparse
import csv
from kayle_grundy import grundy_sequence


def main():
    parser = argparse.ArgumentParser(description="Compute Kayles Grundy numbers 0..N")
    parser.add_argument("-n", "--max", type=int, default=20, help="Maximum pile size (default 20)")
    parser.add_argument("-o", "--out", type=str, default=None, help="Optional CSV output file")
    args = parser.parse_args()

    seq = grundy_sequence(args.max)

    print("Position,Grundy")
    for i, g in enumerate(seq):
        print(f"{i},{g}")

    if args.out:
        with open(args.out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["position", "grundy"])
            for i, g in enumerate(seq):
                w.writerow([i, g])
        print(f"Wrote CSV to {args.out}")


if __name__ == "__main__":
    main()

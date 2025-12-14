# sparse-ruler-n-p-position

programs to check game positions and Grundy numbers. no AI/ML—just plain code.

## main bits
- `sparse.n.p-position.py`: sparse ruler N/P and Grundy, can emit DOT/PNG trees.
- `grundy#Kayle/`: Kayles Grundy calculator + small CLI.
- `scripts/`: helpers for batch Grundy, DOT export, bitmask solver, comparisons.

## run quick
```bash
python sparse.n.p-position.py           # interactive sparse ruler
python grundy#Kayle/compute_grundy.py   # Kayles sequence 0..20
python scripts/generate_dots.py         # regenerate DOT trees
```

python 3.10+; Graphviz `dot` only needed for PNGs.

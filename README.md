# sparse-ruler-n-p-position

programs to check game positions and Grundy numbers. no AI/ML—just plain code.

## main bits
- `sparse.n.p-position.py`: sparse ruler N/P and Grundy, can emit DOT/PNG trees.
- `grundy#Kayle/`: Kayles Grundy calculator + small CLI (first test case to apply to sparse)
- `scripts/`: helpers for batch Grundy, DOT export, bitmask solver

## run quick
```bash
python sparse.n.p-position.py           
python grundy#Kayle/compute_grundy.py  
python scripts/generate_dots.py        
```


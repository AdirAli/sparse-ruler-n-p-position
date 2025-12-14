# Commands Quick Guide

Simple, copy-paste commands to get output from this repo. Python 3.10+ is assumed. Graphviz `dot` is only needed for PNG images.

## Sparse ruler (interactive)
```bash
auth python sparse.n.p-position.py
```
Follow the prompt: enter a sequence like `0123` or `0,1,2,3`. Prints N/P summary, start Grundy, and writes a DOT (and PNG if `dot` is available) into `game_tree/`.

## Generate decision trees (DOT)
```bash
python scripts/generate_dots.py
```
Writes DOT files like `decision_tree_0123.dot` in the current folder. To render PNG:
```bash
dot -Tpng decision_tree_0123.dot -o game_tree/decision_tree_0123.png
```

## Kayles Grundy (sequence 0..N)
```bash
python grundy#Kayle/compute_grundy.py -n 30
```
CSV output:
```bash
python grundy#Kayle/compute_grundy.py -n 30 -o grundy.csv
```

## Universe start Grundy table
```bash
python scripts/generate_universe_grundy.py 0 20
```
Creates `universe_grundy.txt` with `size\tstart_grundy`. Per-size timeout can be changed:
```bash
python scripts/generate_universe_grundy.py 0 50 -t 10
```

## Bitmask DP solver (fast start Grundy for 0..N)
```bash
python scripts/grundy_bitmask.py 12
```
Prints `start_grundy(12) = G (time X.XXXs)`.

## Compare solvers (optional)
If `scripts/test_bitmask.py` exists:
```bash
python scripts/test_bitmask.py 1 20
```
Shows bitmask vs original values and times.

import importlib.machinery
import importlib.util
from pathlib import Path

# Load the main script as a module by filename (it won't run main() because
# __name__ will be set to the module name).
src = Path(__file__).resolve().parents[1] / "sparse.n.p-position.py"
loader = importlib.machinery.SourceFileLoader("sparse_module", str(src))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
loader.exec_module(mod)

# universes to generate (as strings matching your earlier format)
universes = ["01", "012", "0123", "01234", "012345"]

for seq in universes:
    u = mod.parse_sequence(seq)
    labels = mod.classify_all_states(u)
    out = f"decision_tree_{''.join(str(x) for x in u)}.dot"
    mod.export_dot(labels, u, out)

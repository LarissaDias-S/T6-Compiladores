import pathlib
import sys
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py"

spec = importlib.util.spec_from_file_location("mldeclara_main", MAIN_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

base = ROOT / "casos-de-teste/6.casos_teste_t6"
valid_dir = base / "1.validos"
invalid_dir = base / "2.invalidos"

results = []

for p in sorted(valid_dir.glob("*.mld")):
    codigo = p.read_text(encoding="utf-8")
    ast = module.compilar(codigo, str(p))
    ok = ast is not None
    results.append((str(p.relative_to(ROOT)), 'valid', ok))

for p in sorted(invalid_dir.glob("*.mld")):
    codigo = p.read_text(encoding="utf-8")
    ast = module.compilar(codigo, str(p))
    ok = ast is None
    results.append((str(p.relative_to(ROOT)), 'invalid', ok))

print("\nSummary:")
all_good = True
for path, kind, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"{status}: {path} ({kind})")
    if not ok:
        all_good = False

if all_good:
    print("\nAll example tests behaved as expected.")
    sys.exit(0)
else:
    print("\nSome examples did not behave as expected. See details above.")
    sys.exit(2)

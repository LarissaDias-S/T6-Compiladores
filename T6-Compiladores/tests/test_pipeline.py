import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py"

spec = importlib.util.spec_from_file_location("mldeclara_main", MAIN_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_semantica_rejeita_programa_invalido():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario
END
FEATURES idade, salario
MODEL clf RandomForest
  n_estimators = 100
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''

    ast = module.compilar(codigo, "teste_invalido.mld")
    assert ast is None


def test_geracao_de_codigo_retorna_texto():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario, compra
END
TARGET_VAR compra
FEATURES idade, salario
MODEL clf RandomForest
  n_estimators = 100
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''

    ast = module.compilar(codigo, "teste_valido.mld")
    assert ast is not None
    assert ast.target_var == "compra"

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py"


def load_main_module():
    spec = importlib.util.spec_from_file_location("mldeclara_main", MAIN_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def build_programa(source: str):
    module = load_main_module()
    return module.compilar(source, "teste_semantico.mld")


def test_programa_valido_passa_na_semantica():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario, compra
END
TARGET_VAR compra
FEATURES idade, salario
MODEL clf RandomForest
  n_estimators = 100
  max_depth = 3
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is not None


def test_target_var_nao_declarada_eh_erro_semantico():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario
END
TARGET_VAR compra
FEATURES idade, salario
MODEL clf RandomForest
  n_estimators = 100
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is None


def test_feature_nao_declarada_eh_erro_semantico():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario
END
TARGET_VAR salario
FEATURES idade, renda
MODEL clf RandomForest
  n_estimators = 100
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is None


def test_hiperparametro_invalido_eh_erro_semantico():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario, compra
END
TARGET_VAR compra
FEATURES idade, salario
MODEL clf RandomForest
  max_depth = -2
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is None


def test_hiperparametro_desconhecido_eh_erro_semantico():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario, compra
END
TARGET_VAR compra
FEATURES idade, salario
MODEL clf RandomForest
  foo = 3
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is None


def test_metrica_incompativel_com_modelo_eh_erro_semantico():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario, compra
END
TARGET_VAR compra
FEATURES idade, salario
MODEL reg LinearRegression
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is None


def test_features_duplicadas_eh_erro_semantico():
    codigo = '''
DATASET "dados.csv"
  COLUMNS idade, salario, compra
END
TARGET_VAR compra
FEATURES idade, idade
MODEL clf RandomForest
  n_estimators = 100
END
METRICS accuracy
OUTPUT "modelo.pkl"
'''
    ast = build_programa(codigo)
    assert ast is None


def test_output_com_extensao_invalida_eh_erro_semantico():
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
OUTPUT "modelo.txt"
'''
    ast = build_programa(codigo)
    assert ast is None

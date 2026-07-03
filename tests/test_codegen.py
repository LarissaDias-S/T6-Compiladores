"""Testes de geração de código (GCI) e execução dos scripts gerados."""

import importlib.util
import io
import pathlib
import subprocess
import sys
import textwrap

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MLDECLARA_DIR = ROOT / "src/main/python/br/ufscar/dc/compiladores/mldeclara"
CODEGEN_DIR = ROOT / "tests/codegen"
OUTPUT_DIR = CODEGEN_DIR / "output"


def _load_module(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_codegen():
    if str(MLDECLARA_DIR) not in sys.path:
        sys.path.insert(0, str(MLDECLARA_DIR))
    return _load_module("mldeclara_codegen", MLDECLARA_DIR / "codegen.py")


def _load_main():
    return _load_module("mldeclara_main", MLDECLARA_DIR / "main.py")


def _build_ast_from_mld(relative_path: str):
    mld_path = ROOT / relative_path
    source = mld_path.read_text(encoding="utf-8")
    main = _load_main()
    buffer = io.StringIO()
    stdout = sys.stdout
    sys.stdout = buffer
    try:
        ast = main.compilar(source, str(mld_path))
    finally:
        sys.stdout = stdout
    return ast, buffer.getvalue()


def _generate_and_run(relative_mld: str) -> subprocess.CompletedProcess:
    ast, _ = _build_ast_from_mld(relative_mld)
    assert ast is not None

    codegen = _load_codegen()
    script = codegen.CodeGenerator().gerar(ast)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    script_path = OUTPUT_DIR / "generated_script.py"
    script_path.write_text(script, encoding="utf-8")

    return subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.fixture(autouse=True)
def cleanup_output():
    yield
    if OUTPUT_DIR.exists():
        for pkl in OUTPUT_DIR.glob("*.pkl"):
            pkl.unlink(missing_ok=True)
        for py in OUTPUT_DIR.glob("generated_script.py"):
            py.unlink(missing_ok=True)


def test_codigo_gerado_contem_etapas_principais():
    ast, _ = _build_ast_from_mld("tests/codegen/programs/classification.mld")
    assert ast is not None

    codegen = _load_codegen()
    script = codegen.CodeGenerator().gerar(ast)

    assert "pd.read_csv" in script
    assert "train_test_split" in script
    assert "RandomForestClassifier" in script
    assert "joblib.dump" in script
    assert "accuracy_score" in script


def test_execucao_classificacao():
    result = _generate_and_run("tests/codegen/programs/classification.mld")
    assert result.returncode == 0, result.stderr
    assert "accuracy:" in result.stdout
    assert "f1_score:" in result.stdout
    assert "Modelo salvo em:" in result.stdout
    assert (OUTPUT_DIR / "classification_model.pkl").exists()


def test_execucao_regressao():
    result = _generate_and_run("tests/codegen/programs/regression.mld")
    assert result.returncode == 0, result.stderr
    assert "RMSE:" in result.stdout
    assert "MAE:" in result.stdout
    assert "R2:" in result.stdout
    assert (OUTPUT_DIR / "regression_model.pkl").exists()


def test_metricas_regressao_sao_numericas():
    result = _generate_and_run("tests/codegen/programs/regression.mld")
    assert result.returncode == 0, result.stderr

    for line in result.stdout.splitlines():
        if line.strip().startswith("R2:"):
            value = float(line.split(":")[-1].strip())
            assert -1.0 <= value <= 1.0


def test_pipeline_completo_via_main():
    """Valida ALS → AS → GCI para um programa .mld válido."""
    source = textwrap.dedent(
        """
        DATASET "tests/codegen/data/classification.csv"
          COLUMNS idade, salario, regiao, comprou
        END
        TARGET_VAR comprou
        FEATURES idade, salario, regiao
        MODEL clf RandomForest
          n_estimators = 30
        END
        METRICS accuracy
        OUTPUT "tests/codegen/output/pipeline_model.pkl"
        """
    ).strip()

    main = _load_main()
    buffer = io.StringIO()
    stdout = sys.stdout
    sys.stdout = buffer
    try:
        ast = main.compilar(source, "pipeline.mld")
    finally:
        sys.stdout = stdout

    assert ast is not None
    generated = buffer.getvalue()
    assert "RandomForestClassifier" in generated
    assert "joblib.dump" in generated

"""Geração de código Python a partir da AST validada de ML-Declara."""

from __future__ import annotations
from typing import Dict, List, Set, Tuple
from mld_ast import HiperparametroNode, ModeloNode, ProgramaNode

_ALGORITMO_IMPORTS: Dict[str, Tuple[str, str]] = {
    "RandomForest": ("sklearn.ensemble", "RandomForestClassifier"),
    "XGBoost": ("xgboost", "XGBClassifier"),
    "LinearRegression": ("sklearn.linear_model", "LinearRegression"),
    "LogisticRegression": ("sklearn.linear_model", "LogisticRegression"),
    "SVM": ("sklearn.svm", "SVC"),
}

_METRICA_IMPORTS: Dict[str, Tuple[str, str]] = {
    "accuracy": ("sklearn.metrics", "accuracy_score"),
    "f1_score": ("sklearn.metrics", "f1_score"),
    "precision": ("sklearn.metrics", "precision_score"),
    "recall": ("sklearn.metrics", "recall_score"),
    "RMSE": ("sklearn.metrics", "mean_squared_error"),
    "MAE": ("sklearn.metrics", "mean_absolute_error"),
    "R2": ("sklearn.metrics", "r2_score"),
}

_MODELOS_CLASSIFICACAO = {"RandomForest", "XGBoost", "LogisticRegression", "SVM"}
_TEST_SIZE = 0.2
_RANDOM_STATE = 42

class CodeGenerator:
    """Gera um script Python completo a partir da AST."""

    def gerar(self, ast: ProgramaNode) -> str:
        linhas: List[str] = []
        linhas.extend(self._gerar_cabecalho())
        linhas.extend(self._gerar_imports(ast))
        linhas.append("")
        linhas.extend(self._gerar_carregamento(ast))
        linhas.append("")
        linhas.extend(self._gerar_preprocessamento(ast))
        linhas.append("")
        linhas.extend(self._gerar_split())
        linhas.append("")

        for modelo in ast.modelos:
            linhas.extend(self._gerar_treinamento(modelo, ast.metricas))
            linhas.append("")

        ultimo_modelo = ast.modelos[-1].nome
        linhas.extend(self._gerar_serializacao(ultimo_modelo, ast.output_path))
        return "\n".join(linhas)

    def _gerar_cabecalho(self) -> List[str]:
        return ['"""', "Script gerado automaticamente pelo compilador ML-Declara.", '"""', ""]

    def _gerar_imports(self, ast: ProgramaNode) -> List[str]:
        linhas = ["import os", "import joblib", "import pandas as pd", "import numpy as np", "from sklearn.model_selection import train_test_split"]

        modulos_modelo: Set[Tuple[str, str]] = set()
        for modelo in ast.modelos:
            alg_limpo = str(modelo.algoritmo).replace('"', '').replace("'", "").strip()
            if alg_limpo in _ALGORITMO_IMPORTS:
                modulos_modelo.add(_ALGORITMO_IMPORTS[alg_limpo])

        for modulo, classe in sorted(modulos_modelo):
            linhas.append(f"from {modulo} import {classe}")

        modulos_metrica: Set[Tuple[str, str]] = set()
        for metrica in ast.metricas:
            if metrica in _METRICA_IMPORTS:
                modulos_metrica.add(_METRICA_IMPORTS[metrica])

        for modulo, funcao in sorted(modulos_metrica):
            linhas.append(f"from {modulo} import {funcao}")

        if self._precisa_label_encoder(ast):
            linhas.append("from sklearn.preprocessing import LabelEncoder")

        return linhas

    def _precisa_label_encoder(self, ast: ProgramaNode) -> bool:
        return any(str(m.algoritmo).replace('"', '').replace("'", "").strip() in _MODELOS_CLASSIFICACAO for m in ast.modelos)

    def _gerar_carregamento(self, ast: ProgramaNode) -> List[str]:
        return [
            "# --- Carregamento do dataset ---",
            f"DATASET_PATH = {ast.dataset.caminho!r}",
            f"TARGET_VAR = {ast.target_var!r}",
            f"FEATURES = {ast.features!r}",
            f"OUTPUT_PATH = {ast.output_path!r}",
            "",
            "df = pd.read_csv(DATASET_PATH)",
        ]

    def _gerar_preprocessamento(self, ast: ProgramaNode) -> List[str]:
        linhas = [
            "# --- Pré-processamento ---",
            "X = df[FEATURES].copy()",
            "y = df[TARGET_VAR].copy()",
            "",
            "cat_cols = X.select_dtypes(include=['object', 'string', 'category']).columns.tolist()",
            "if cat_cols:",
            "    X = pd.get_dummies(X, columns=cat_cols, drop_first=False)",
        ]
        if self._precisa_label_encoder(ast):
            linhas.extend([
                "",
                "if y.dtype == 'object' or str(y.dtype) == 'string':",
                "    label_encoder = LabelEncoder()",
                "    y = label_encoder.fit_transform(y)",
            ])
        return linhas

    def _gerar_split(self) -> List[str]:
        return [
            "# --- Divisão treino/teste ---",
            f"X_train, X_test, y_train, y_test = train_test_split(",
            f"    X, y, test_size={_TEST_SIZE}, random_state={_RANDOM_STATE}",
            ")",
        ]

    def _gerar_treinamento(self, modelo: ModeloNode, metricas: List[str]) -> List[str]:
        alg_limpo = str(modelo.algoritmo).replace('"', '').replace("'", "").strip()
        
        if alg_limpo in _ALGORITMO_IMPORTS:
            classe = _ALGORITMO_IMPORTS[alg_limpo][1]
        else:
            classe = alg_limpo

        hiperparams = ", ".join(self._formatar_hiperparametro(h) for h in modelo.hiperparametros)
        args = hiperparams if hiperparams else ""

        linhas = [
            f"# --- Modelo: {modelo.nome} ---",
            f"{modelo.nome} = {classe}({args})" if args else f"{modelo.nome} = {classe}()",
            f"{modelo.nome}.fit(X_train, y_train)",
            f"y_pred_{modelo.nome} = {modelo.nome}.predict(X_test)",
            "",
            f"print('=== Métricas — {modelo.nome} ({alg_limpo}) ===')",
        ]

        for metrica in metricas:
            linhas.extend(self._gerar_calculo_metrica(metrica, modelo.nome, alg_limpo))

        return linhas

    def _gerar_calculo_metrica(self, metrica: str, nome_modelo: str, algoritmo: str) -> List[str]:
        y_pred = f"y_pred_{nome_modelo}"
        is_classificacao = algoritmo in _MODELOS_CLASSIFICACAO

        if metrica == "accuracy":
            return [f"print(f'  accuracy: {{accuracy_score(y_test, {y_pred}):.4f}}')"]
        if metrica == "f1_score":
            avg = '"binary"' if is_classificacao else '"weighted"'
            return [f"print(f'  f1_score: {{f1_score(y_test, {y_pred}, average={avg}):.4f}}')"]
        if metrica == "precision":
            avg = '"binary"' if is_classificacao else '"weighted"'
            return [f"print(f'  precision: {{precision_score(y_test, {y_pred}, average={avg}, zero_division=0):.4f}}')"]
        if metrica == "recall":
            avg = '"binary"' if is_classificacao else '"weighted"'
            return [f"print(f'  recall: {{recall_score(y_test, {y_pred}, average={avg}, zero_division=0):.4f}}')"]
        if metrica == "RMSE":
            return [f"_rmse = np.sqrt(mean_squared_error(y_test, {y_pred}))", "print(f'  RMSE: {{_rmse:.4f}}')"]
        if metrica == "MAE":
            return [f"print(f'  MAE: {{mean_absolute_error(y_test, {y_pred}):.4f}}')"]
        if metrica == "R2":
            return [f"print(f'  R2: {{r2_score(y_test, {y_pred}):.4f}}')"]
        return []

    def _gerar_serializacao(self, nome_modelo: str, output_path: str) -> List[str]:
        return [
            "# --- Serialização do modelo ---",
            f"os.makedirs(os.path.dirname(OUTPUT_PATH) or '.', exist_ok=True)",
            f"joblib.dump({nome_modelo}, OUTPUT_PATH)",
            f"print(f'Modelo saved: {{OUTPUT_PATH}}')",
        ]

    def _gerar_algoritmo(self, modelo: ModeloNode) -> str:
        alg_limpo = str(modelo.algoritmo).replace('"', '').replace("'", "").strip()
        classe = _ALGORITMO_IMPORTS.get(alg_limpo, (None, alg_limpo))[1]
        hiperparams = ", ".join(self._formatar_hiperparametro(h) for h in modelo.hiperparametros)
        if hiperparams:
            return f"{classe}({hiperparams})"
        return f"{classe}()"

    def _formatar_hiperparametro(self, hiper: HiperparametroNode) -> str:
        if hiper.tipo == "str":
            return f"{hiper.nome}={hiper.valor!r}"
        return f"{hiper.nome}={hiper.valor}"
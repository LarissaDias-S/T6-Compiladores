"""Geração de código Python a partir da AST de ML-Declara."""

from typing import List

from mld_ast import HiperparametroNode, ModeloNode, ProgramaNode


class CodeGenerator:
    """Gera um script Python simples a partir da AST."""

    def gerar(self, ast: ProgramaNode) -> str:
        linhas: List[str] = []
        linhas.append("import pandas as pd")
        linhas.append("from sklearn.pipeline import make_pipeline")
        linhas.append("")
        linhas.append("# Código gerado automaticamente a partir de ML-Declara")
        linhas.append("# Dataset")
        linhas.append(f"dataset_path = {ast.dataset.caminho!r}")
        linhas.append(f"columns = {ast.dataset.colunas}")
        linhas.append(f"target_var = {ast.target_var!r}")
        linhas.append(f"features = {ast.features}")
        linhas.append("")
        linhas.append("# Modelos")
        for modelo in ast.modelos:
            linhas.append(f"{modelo.nome} = {self._gerar_algoritmo(modelo)}")
        linhas.append("")
        linhas.append("# Métricas")
        linhas.append(f"metrics = {ast.metricas}")
        linhas.append(f"output_path = {ast.output_path!r}")
        linhas.append("")
        linhas.append("print('Pipeline ML-Declara gerado com sucesso')")
        return "\n".join(linhas)

    def _gerar_algoritmo(self, modelo: ModeloNode) -> str:
        algoritmo = modelo.algoritmo
        hiperparams = ", ".join(self._formatar_hiperparametro(h) for h in modelo.hiperparametros)
        if hiperparams:
            return f"{algoritmo}({hiperparams})"
        return f"{algoritmo}()"

    def _formatar_hiperparametro(self, hiper: HiperparametroNode) -> str:
        if hiper.tipo == "str":
            return f"{hiper.nome}={hiper.valor!r}"
        return f"{hiper.nome}={hiper.valor}"

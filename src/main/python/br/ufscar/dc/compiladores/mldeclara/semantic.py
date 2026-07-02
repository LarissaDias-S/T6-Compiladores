"""Módulo de análise semântica para a linguagem ML-Declara."""

from typing import List

from mld_ast import ProgramaNode


class SemanticVisitor:
    """Valida a consistência do programa após a construção da AST."""

    def __init__(self) -> None:
        self.erros: List[str] = []

    def verificar(self, ast: ProgramaNode) -> List[str]:
        """Retorna a lista de erros semânticos encontrados."""
        self.erros = []

        if ast is None:
            self.erros.append("AST inválida: programa não foi construído.")
            return self.erros

        self._validar_dataset(ast)
        self._validar_target_var(ast)
        self._validar_features(ast)
        self._validar_modelos(ast)
        self._validar_metricas(ast)
        self._validar_output(ast)

        return self.erros

    def _validar_dataset(self, ast: ProgramaNode) -> None:
        if not ast.dataset:
            self.erros.append("O programa deve declarar um bloco DATASET.")
            return

        if not ast.dataset.colunas:
            self.erros.append("O bloco DATASET deve declarar pelo menos uma coluna.")

    def _validar_target_var(self, ast: ProgramaNode) -> None:
        if not ast.target_var:
            self.erros.append("A diretiva TARGET_VAR é obrigatória.")
            return

        colunas = set(ast.dataset.colunas if ast.dataset else [])
        if ast.target_var not in colunas:
            self.erros.append(
                f"A variável alvo '{ast.target_var}' não foi declarada no bloco DATASET."
            )

    def _validar_features(self, ast: ProgramaNode) -> None:
        if not ast.features:
            self.erros.append("A diretiva FEATURES é obrigatória.")
            return

        colunas = set(ast.dataset.colunas if ast.dataset else [])
        for feature in ast.features:
            if feature not in colunas:
                self.erros.append(
                    f"A feature '{feature}' não foi declarada no bloco DATASET."
                )

        if len(ast.features) != len(set(ast.features)):
            self.erros.append("A lista de FEATURES contém nomes duplicados.")

    def _validar_modelos(self, ast: ProgramaNode) -> None:
        if not ast.modelos:
            self.erros.append("O programa deve declarar pelo menos um bloco MODEL.")

        for modelo in ast.modelos:
            if not modelo.nome:
                self.erros.append("Cada bloco MODEL precisa ter um nome.")
            if not modelo.algoritmo:
                self.erros.append(f"O modelo '{modelo.nome}' não declarou um algoritmo.")

    def _validar_metricas(self, ast: ProgramaNode) -> None:
        if not ast.metricas:
            self.erros.append("A diretiva METRICS é obrigatória.")
            return

        metricas_validas = {"accuracy", "f1_score", "precision", "recall", "RMSE", "MAE", "R2"}
        for metrica in ast.metricas:
            if metrica not in metricas_validas:
                self.erros.append(f"A métrica '{metrica}' não é suportada.")

    def _validar_output(self, ast: ProgramaNode) -> None:
        if not ast.output_path:
            self.erros.append("A diretiva OUTPUT é obrigatória.")
            return

        if not ast.output_path.endswith((".pkl", ".joblib")):
            self.erros.append("O caminho de OUTPUT deve terminar com .pkl ou .joblib.")

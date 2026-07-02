"""Módulo de análise semântica para a linguagem ML-Declara."""

from typing import Dict, List, Set

from mld_ast import HiperparametroNode, ModeloNode, ProgramaNode


class SemanticVisitor:
    """Valida a consistência do programa após a construção da AST."""

    def __init__(self) -> None:
        self.erros: List[str] = []
        self.tabela_simbolos: Dict[str, Dict[str, str]] = {}
        self.modelo_para_hiperparams = {
            "RandomForest": {"n_estimators": "int", "max_depth": "int", "random_state": "int"},
            "XGBoost": {"n_estimators": "int", "max_depth": "int", "learning_rate": "float"},
            "LinearRegression": {},
            "LogisticRegression": {"max_iter": "int", "C": "float"},
            "SVM": {"C": "float", "kernel": "str"},
        }
        self.metricas_por_modelo = {
            "classificacao": {"accuracy", "f1_score", "precision", "recall"},
            "regressao": {"RMSE", "MAE", "R2"},
        }

    def verificar(self, ast: ProgramaNode) -> List[str]:
        """Retorna a lista de erros semânticos encontrados."""
        """
        Executa todas as validações semânticas no AST fornecido.

        Args:
            ast: `ProgramaNode` construído pelo `ASTBuilder`.

        Returns:
            Lista de strings com as mensagens de erro (vazia se sem erros).
        """
        self.erros = []
        self.tabela_simbolos = {}

        if ast is None:
            self.erros.append("Erro semântico: AST inválida — programa não foi construído.")
            return self.erros

        self._validar_dataset(ast)
        self._validar_target_var(ast)
        self._validar_features(ast)
        self._validar_modelos(ast)
        self._validar_metricas(ast)
        self._validar_output(ast)

        return self.erros

    def _validar_dataset(self, ast: ProgramaNode) -> None:
        """Valida a presença do bloco DATASET e popula a tabela de símbolos.

        Adiciona cada coluna declarada em `ast.dataset.colunas` na
        `self.tabela_simbolos` para uso pelas demais verificações.
        """
        if not ast.dataset:
            self.erros.append("Erro semântico: o programa deve declarar um bloco DATASET.")
            return

        if not ast.dataset.colunas:
            self.erros.append("Erro semântico: o bloco DATASET deve declarar pelo menos uma coluna.")
            return

        for coluna in ast.dataset.colunas:
            self.tabela_simbolos[coluna] = {"tipo": "coluna", "origem": "dataset"}

    def _validar_target_var(self, ast: ProgramaNode) -> None:
        """Valida que a diretiva TARGET_VAR esteja presente e seja uma coluna válida."""
        if not ast.target_var:
            self.erros.append("Erro semântico: a diretiva TARGET_VAR é obrigatória.")
            return

        colunas = set(ast.dataset.colunas if ast.dataset else [])
        if ast.target_var not in colunas:
            self.erros.append(
                f"Erro semântico: a variável alvo '{ast.target_var}' não foi declarada no bloco DATASET."
            )

    def _validar_features(self, ast: ProgramaNode) -> None:
        """Valida a diretiva FEATURES: existência, presença no dataset e duplicatas."""
        if not ast.features:
            self.erros.append("Erro semântico: a diretiva FEATURES é obrigatória.")
            return

        colunas = set(ast.dataset.colunas if ast.dataset else [])
        for feature in ast.features:
            if feature not in colunas:
                self.erros.append(
                    f"Erro semântico: a feature '{feature}' não foi declarada no bloco DATASET."
                )
            if feature == ast.target_var:
                self.erros.append(
                    f"Erro semântico: a feature '{feature}' não pode coincidir com a variável alvo."
                )

        if len(ast.features) != len(set(ast.features)):
            self.erros.append("Erro semântico: a lista de FEATURES contém nomes duplicados.")

    def _validar_modelos(self, ast: ProgramaNode) -> None:
        """Valida blocos MODEL: nome, algoritmo suportado e hiperparâmetros."""
        if not ast.modelos:
            self.erros.append("Erro semântico: o programa deve declarar pelo menos um bloco MODEL.")
            return

        for modelo in ast.modelos:
            if not modelo.nome:
                self.erros.append("Erro semântico: cada bloco MODEL precisa ter um nome.")
                continue

            if modelo.algoritmo not in self.modelo_para_hiperparams:
                self.erros.append(
                    f"Erro semântico: o algoritmo '{modelo.algoritmo}' não é suportado."
                )
                continue

            self._validar_hiperparametros(modelo)

    def _validar_hiperparametros(self, modelo: ModeloNode) -> None:
        """Verifica hiperparâmetros de um `ModeloNode` contra a tabela por-modelo.

        Valida tanto a presença do hiperparâmetro quanto o tipo/intervalo do valor.
        """
        hiperparams_validos = self.modelo_para_hiperparams.get(modelo.algoritmo, {})
        for hiper in modelo.hiperparametros:
            if hiper.nome not in hiperparams_validos:
                self.erros.append(
                    f"Erro semântico: o hiperparâmetro '{hiper.nome}' não é válido para o modelo '{modelo.algoritmo}'."
                )
                continue

            esperado = hiperparams_validos[hiper.nome]
            if esperado == "int":
                try:
                    valor = int(hiper.valor)
                except ValueError:
                    self.erros.append(
                        f"Erro semântico: o hiperparâmetro '{hiper.nome}' deve ser um inteiro."
                    )
                    continue
                if valor < 1:
                    self.erros.append(
                        f"Erro semântico: o hiperparâmetro '{hiper.nome}' deve ser maior ou igual a 1."
                    )
            elif esperado == "float":
                try:
                    valor = float(hiper.valor)
                except ValueError:
                    self.erros.append(
                        f"Erro semântico: o hiperparâmetro '{hiper.nome}' deve ser um número decimal."
                    )
                    continue
                if valor <= 0:
                    self.erros.append(
                        f"Erro semântico: o hiperparâmetro '{hiper.nome}' deve ser maior que zero."
                    )

    def _validar_metricas(self, ast: ProgramaNode) -> None:
        """Valida a diretiva METRICS: métricas conhecidas, repetição e compatibilidade."""
        if not ast.metricas:
            self.erros.append("Erro semântico: a diretiva METRICS é obrigatória.")
            return

        metricas_validas = {"accuracy", "f1_score", "precision", "recall", "RMSE", "MAE", "R2"}
        metricas_vistas: Set[str] = set()
        for metrica in ast.metricas:
            if metrica not in metricas_validas:
                self.erros.append(f"Erro semântico: a métrica '{metrica}' não é suportada.")
                continue
            if metrica in metricas_vistas:
                self.erros.append(f"Erro semântico: a métrica '{metrica}' foi repetida.")
            metricas_vistas.add(metrica)

        if not ast.modelos:
            return

        for modelo in ast.modelos:
            tipo_modelo = self._classificar_modelo(modelo.algoritmo)
            for metrica in ast.metricas:
                if tipo_modelo == "classificacao" and metrica in self.metricas_por_modelo["regressao"]:
                    self.erros.append(
                        f"Erro semântico: a métrica '{metrica}' não é compatível com o modelo '{modelo.algoritmo}'."
                    )
                elif tipo_modelo == "regressao" and metrica in self.metricas_por_modelo["classificacao"]:
                    self.erros.append(
                        f"Erro semântico: a métrica '{metrica}' não é compatível com o modelo '{modelo.algoritmo}'."
                    )

    def _classificar_modelo(self, algoritmo: str) -> str:
        """Classifica um algoritmo em 'classificacao' ou 'regressao'."""
        modelos_classificacao = {"RandomForest", "XGBoost", "LogisticRegression", "SVM"}
        if algoritmo in modelos_classificacao:
            return "classificacao"
        return "regressao"

    def _validar_output(self, ast: ProgramaNode) -> None:
        """Valida a diretiva OUTPUT e verifica a extensão do arquivo de saída."""
        if not ast.output_path:
            self.erros.append("Erro semântico: a diretiva OUTPUT é obrigatória.")
            return

        if not ast.output_path.endswith((".pkl", ".joblib")):
            self.erros.append("Erro semântico: o caminho de OUTPUT deve terminar com .pkl ou .joblib.")

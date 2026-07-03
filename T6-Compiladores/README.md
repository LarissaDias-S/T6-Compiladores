# T6 - ML-Declara

Este repositório contém a implementação da linguagem declarativa ML-Declara para a disciplina de Construção de Compiladores, utilizando ANTLR4 para análise léxica e sintática.

## Integrantes do Grupo
- Bruna Matias de Lima - RA: 820582
- Julia Pedro Silva - RA: 820869
- Larissa Dias da Silva - RA: 800204

## Objetivo do Projeto
O projeto implementa um compilador para programas em formato .mld com suporte a:
- bloco DATASET
- diretivas TARGET_VAR e FEATURES
- um ou mais blocos MODEL
- diretiva METRICS
- diretiva OUTPUT

A implementação atual cobre a etapa de ALS (análise léxica e sintática), a construção de uma AST simplificada e o tratamento de erros com mensagens claras.

## Status Atual
### Implementado
- Gramática ANTLR4 completa em [src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4](src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4)
- Lexer, Parser e Visitor gerados para Python
- Visitor responsável pela construção da AST em [src/main/python/br/ufscar/dc/compiladores/mldeclara/ast_builder.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/ast_builder.py)
- Definição dos nós da AST em [src/main/python/br/ufscar/dc/compiladores/mldeclara/mld_ast.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/mld_ast.py)
- Listener customizado de erros sintáticos em [src/main/python/br/ufscar/dc/compiladores/mldeclara/error_listener.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/error_listener.py)
- Ponto de entrada do compilador em [src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py)
- Casos de teste válidos e inválidos em [casos-de-teste/6.casos_teste_t6](casos-de-teste/6.casos_teste_t6)
- Script de execução dos testes em [rodar_testes_t6.bat](rodar_testes_t6.bat)

### Pipeline completo (ALS → AS → GCI)
- Análise semântica: implementada em [semantic.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/semantic.py)
- Geração de código: implementada em [codegen.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/codegen.py)
- Integração completa: `.mld` → parsing → AST → validação semântica → script Python executável
- Testes de codegen: [tests/test_codegen.py](tests/test_codegen.py) e [tests/codegen/](tests/codegen/)

## Estrutura do Repositório
- [src/main/antlr4_mldeclara](src/main/antlr4_mldeclara) — gramática ANTLR4
- [src/main/python/br/ufscar/dc/compiladores/mldeclara](src/main/python/br/ufscar/dc/compiladores/mldeclara) — implementação Python do compilador
- [casos-de-teste/6.casos_teste_t6](casos-de-teste/6.casos_teste_t6) — programas de teste
- [rodar_testes_t6.bat](rodar_testes_t6.bat) — execução automática dos testes

## Sintaxe Suportada
A gramática atual aceita os seguintes elementos:
- DATASET "caminho.csv" com COLUMNS ... END
- TARGET_VAR <nome>
- FEATURES <lista de nomes>
- MODEL <nome> <algoritmo> [hiperparâmetros] END
- METRICS <lista de métricas>
- OUTPUT "caminho"
- Comentários com // ou #
- Literais: strings, identificadores, inteiros e decimais

### Algoritmos aceitos
- RandomForest
- XGBoost
- LinearRegression
- LogisticRegression
- SVM

### Métricas aceitas
- accuracy
- f1_score
- precision
- recall
- RMSE
- MAE
- R2

## Como Executar
### Requisitos
- Python 3
- pacote ANTLR4 para Python:

```bash
pip install antlr4-python3-runtime pandas scikit-learn xgboost joblib
```

### Execução do compilador
Na raiz do projeto, execute:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py caminho/para/arquivo.mld
```

Exemplo:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py casos-de-teste/6.casos_teste_t6/1.validos/v01_random_forest_basico.mld
```

Se o arquivo for válido, o compilador gera um script Python completo na saída padrão (stdout). Redirecione para um arquivo `.py` e execute-o para treinar o modelo:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py tests/codegen/programs/classification.mld > treino.py
python treino.py
```

Se houver problemas léxicos, sintáticos ou semânticos, o compilador exibe mensagens claras e encerra com código de saída 1.

## Testes
Os testes do trabalho estão organizados em duas pastas:
- [casos-de-teste/6.casos_teste_t6/1.validos](casos-de-teste/6.casos_teste_t6/1.validos) — programas que devem ser aceitos
- [casos-de-teste/6.casos_teste_t6/2.invalidos](casos-de-teste/6.casos_teste_t6/2.invalidos) — programas com erros propositalmente inseridos

No Windows, a validação pode ser rodada com:

```bat
rodar_testes_t6.bat
```

### Como regenerar o Lexer/Parser com ANTLR

Se você precisar regenerar os arquivos do Lexer/Parser a partir da gramática (`MLDeclara.g4`), instale o jar do ANTLR e execute (exemplo usando a versão 4.13.2):

```bash
# baixar o jar do ANTLR (exemplo):
wget https://www.antlr.org/download/antlr-4.13.2-complete.jar

# gerar para Python3 (executar no diretório que contém MLDeclara.g4):
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 MLDeclara.g4

# Opcional: mover/organizar os arquivos gerados em src/main/python/... conforme a estrutura do projeto
``` 

Observação: é recomendado Java 11+ e usar a mesma versão do runtime Python (`antlr4-python3-runtime`) compatível com o jar.

### Instalar dependências e rodar testes

Recomenda-se criar um ambiente virtual e instalar dependências via `requirements.txt` (arquivo incluído neste repositório):

```bash
python -m venv .venv
source .venv/bin/activate  # ou `.venv\Scripts\activate` no Windows
pip install -r requirements.txt

# Executar a suíte de testes
python -m pytest -q
```

## Geração de Código (GCI)

O módulo `codegen.py` produz scripts Python com:

- Carregamento do CSV via `pandas.read_csv`
- Separação de features (`X`) e variável alvo (`y`)
- Codificação automática de colunas categóricas (`pd.get_dummies`)
- Split treino/teste 80/20 (`random_state=42`)
- Instanciação do modelo sklearn/xgboost com hiperparâmetros declarados
- Treinamento, predição e impressão das métricas declaradas
- Serialização do último modelo treinado via `joblib.dump`

### Mapeamento algoritmo → classe Python

| ML-Declara | Biblioteca |
|------------|------------|
| RandomForest | `sklearn.ensemble.RandomForestClassifier` |
| XGBoost | `xgboost.XGBClassifier` |
| LinearRegression | `sklearn.linear_model.LinearRegression` |
| LogisticRegression | `sklearn.linear_model.LogisticRegression` |
| SVM | `sklearn.svm.SVC` |

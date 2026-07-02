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

### Em andamento / Observações
- Análise semântica: implementada (ver `src/main/python/br/ufscar/dc/compiladores/mldeclara/semantic.py`)
- Geração de código: implementação inicial presente em `codegen.py`, pode ser refinada
- Integração completa do pipeline: testes automatizados cobrem parsing e semântica

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
pip install antlr4-python3-runtime
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

Se o arquivo for válido, o programa constrói a AST sem reportar erros. Se houver problemas léxicos ou sintáticos, o compilador exibe mensagens com linha e coluna.

## Testes
Os testes do trabalho estão organizados em duas pastas:
- [casos-de-teste/6.casos_teste_t6/1.validos](casos-de-teste/6.casos_teste_t6/1.validos) — programas que devem ser aceitos
- [casos-de-teste/6.casos_teste_t6/2.invalidos](casos-de-teste/6.casos_teste_t6/2.invalidos) — programas com erros propositalmente inseridos

No Windows, a validação pode ser rodada com:

```bat
rodar_testes_t6.bat
```

## Observação
Este README descreve o cenário atual do T6, que concentra-se na análise léxica/sintática, na construção da AST e no tratamento de erros para a linguagem ML-Declara.

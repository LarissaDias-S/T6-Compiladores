# T6 - ML-Declara

Este repositório contém a implementação completa da linguagem declarativa ML-Declara para a disciplina de Construção de Compiladores. O projeto cobre a cadeia completa de processamento de um programa `.mld`: leitura, análise léxica, análise sintática, construção de AST, análise semântica, geração de código Python e testes automatizados.

## Integrantes do Grupo
- Bruna Matias de Lima - RA: 820582
- Julia Pedro Silva - RA: 820869
- Larissa Dias da Silva - RA: 800204

## Objetivo do Projeto
O ML-Declara permite descrever, de forma declarativa, um pipeline simples de Machine Learning com blocos para:
- `DATASET`
- `TARGET_VAR`
- `FEATURES`
- `MODEL`
- `METRICS`
- `OUTPUT`

A partir de um arquivo `.mld`, o compilador gera uma representação intermediária em AST, valida a consistência semântica e produz um código Python inicial como saída.

## Status Final do Projeto
O projeto está completo para a proposta do trabalho, incluindo as atividades da Pessoa 1, Pessoa 2 e Pessoa 3.

### O que está implementado
- Gramática ANTLR4 completa em [src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4](src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4)
- Lexer e Parser gerados para Python
- Visitor para construção da AST em [src/main/python/br/ufscar/dc/compiladores/mldeclara/ast_builder.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/ast_builder.py)
- Definição dos nós da AST em [src/main/python/br/ufscar/dc/compiladores/mldeclara/mld_ast.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/mld_ast.py)
- Análise semântica com validações de consistência em [src/main/python/br/ufscar/dc/compiladores/mldeclara/semantic.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/semantic.py)
- Geração de código Python a partir da AST em [src/main/python/br/ufscar/dc/compiladores/mldeclara/codegen.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/codegen.py)
- Tratamento de erros léxicos e sintáticos com mensagens claras em [src/main/python/br/ufscar/dc/compiladores/mldeclara/error_listener.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/error_listener.py)
- Pipeline principal em [src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py)
- Casos de teste válidos e inválidos em [casos-de-teste/6.casos_teste_t6](casos-de-teste/6.casos_teste_t6)
- Documentação adicional de testes e regras semânticas em [tests/semantic/hiperparams.md](tests/semantic/hiperparams.md), [tests/syntax/README.md](tests/syntax/README.md) e [docs/checklist.md](docs/checklist.md)

## Arquitetura do Projeto
O fluxo do compilador é:
1. Leitura de um arquivo `.mld`
2. Análise léxica e sintática com ANTLR4
3. Construção da AST
4. Validação semântica
5. Geração de um script Python inicial

## Sintaxe Suportada
A linguagem aceita os seguintes elementos:
- `DATASET "caminho.csv"` com `COLUMNS ... END`
- `TARGET_VAR <nome>`
- `FEATURES <lista de nomes>`
- `MODEL <nome> <algoritmo> [hiperparâmetros] END`
- `METRICS <lista de métricas>`
- `OUTPUT "caminho"`
- Comentários com `//` ou `#`
- Literais: strings, identificadores, inteiros e decimais

### Algoritmos aceitos
- `RandomForest`
- `XGBoost`
- `LinearRegression`
- `LogisticRegression`
- `SVM`

### Métricas aceitas
- `accuracy`
- `f1_score`
- `precision`
- `recall`
- `RMSE`
- `MAE`
- `R2`

## Como usar
### Requisitos
- Python 3
- Dependências do projeto

```bash
pip install -r requirements.txt
```

### Executar o compilador
Na raiz do projeto, execute:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py caminho/para/arquivo.mld
```

Exemplo:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py casos-de-teste/6.casos_teste_t6/1.validos/v01_random_forest_basico.mld
```

Se o arquivo for válido, o programa gera a AST e o código Python correspondente. Se houver problemas léxicos, sintáticos ou semânticos, o compilador exibe mensagens com linha, coluna e descrição do problema.

## Exemplos de uso
A pasta [casos-de-teste/6.casos_teste_t6](casos-de-teste/6.casos_teste_t6) contém exemplos válidos e inválidos que demonstram o funcionamento da linguagem.

## Testes
Os testes automatizados do projeto estão em [tests/test_pipeline.py](tests/test_pipeline.py) e [tests/test_semantic.py](tests/test_semantic.py).

Para rodar a suíte:

```bash
python -m pytest -q
```

## Como regenerar o Lexer/Parser com ANTLR
Se for necessário regenerar os arquivos a partir da gramática, use:

```bash
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 MLDeclara.g4
```

> Recomendação: usar Java 11+ e a versão compatível do runtime Python (`antlr4-python3-runtime`).

## Estrutura do Repositório
- [src/main/antlr4_mldeclara](src/main/antlr4_mldeclara) — gramática ANTLR4
- [src/main/python/br/ufscar/dc/compiladores/mldeclara](src/main/python/br/ufscar/dc/compiladores/mldeclara) — implementação Python do compilador
- [tests](tests) — testes e documentação de casos de teste
- [docs](docs) — checklist e documentação do projeto
- [casos-de-teste/6.casos_teste_t6](casos-de-teste/6.casos_teste_t6) — programas de teste válidos e inválidos

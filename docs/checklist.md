# Checklist de Requisitos (ALS e AS)

Mapa rápido dos requisitos da Pessoa 1 (ALS) e Pessoa 2 (AS) e onde estão implementados.

## Pessoa 1 — ALS (Análise Léxica/Sintática)
- Gramática `.g4`: `src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4` — ✅
- Lexer/Parser gerados: `src/main/python/br/ufscar/dc/compiladores/mldeclara/MLDeclaraLexer.py`, `MLDeclaraParser.py` — ✅
- Visitor → AST: `src/main/python/br/ufscar/dc/compiladores/mldeclara/ast_builder.py` — ✅
- ErrorListener customizado: `src/main/python/br/ufscar/dc/compiladores/mldeclara/error_listener.py` — ✅
- Testes sintáticos (casos válidos/inválidos): `casos-de-teste/6.casos_teste_t6` — ✅
- Documentação adicional de sintaxe: `tests/syntax/README.md` — ✅

## Pessoa 2 — AS (Análise Semântica)
- Tabela de modelos e hiperparâmetros: implementada em `semantic.py` e documentada em `tests/semantic/hiperparams.md` — ✅
- Verificações implementadas:
  - TARGET_VAR presente em COLUMNS — ✅
  - FEATURES presentes em COLUMNS e sem coincidência com TARGET_VAR — ✅
  - Validação de hiperparâmetros por modelo (tipo e intervalo) — ✅
  - Consistência modelo × métrica — ✅
  - Duplicatas em FEATURES e métricas repetidas — ✅
  - OUTPUT com extensão válida (.pkl/.joblib) — ✅
- Testes semânticos: `tests/test_semantic.py` — ✅

## Observações / Próximos passos recomendados
- Revisar/expandir `modelo_para_hiperparams` em `semantic.py` se mais hiperparâmetros forem suportados.
- Refinar mensagens de erro para incluir nome do arquivo (atualmente o `main.py` já exibe o nome ao imprimir blocos de erro).
- Implementar validações opcionais: tipo de coluna vs. uso, mais checagens de consistência entre blocos.


## Links úteis
- Gramática: [src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4](src/main/antlr4_mldeclara/br/ufscar/dc/compiladores/mldeclara/MLDeclara.g4)
- AST: [src/main/python/br/ufscar/dc/compiladores/mldeclara/mld_ast.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/mld_ast.py)
- Semântica: [src/main/python/br/ufscar/dc/compiladores/mldeclara/semantic.py](src/main/python/br/ufscar/dc/compiladores/mldeclara/semantic.py)
- Testes: [tests/test_semantic.py](tests/test_semantic.py)

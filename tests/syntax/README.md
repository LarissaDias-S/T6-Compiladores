# Casos de Teste de Sintaxe — ML-Declara

Esta pasta documenta os testes de sintaxe (ALS) usados pelo projeto.

Arquivos relevantes (na pasta `casos-de-teste/6.casos_teste_t6`):
- 1.validos/: cinco exemplos válidos (v01_... v05_...)
- 2.invalidos/: sete exemplos inválidos (e01_... e07_...)

O parser (ANTLR4) e o `ErrorListener` customizado reportam erros léxicos e sintáticos
com linha/coluna e uma mensagem legível. Exemplos de erros sintáticos testados:
- bloco `DATASET` sem `END`
- cadeia literal não fechada
- palavra-chave em caixa errada
- vírgula faltando em listas

Uso rápido para validar um arquivo manualmente:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py casos-de-teste/6.casos_teste_t6/1.validos/v01_random_forest_basico.mld
```

Os testes automatizados em `tests/test_pipeline.py` e `tests/test_semantic.py`
cobrem parse + construção de AST + validações semânticas básicas.

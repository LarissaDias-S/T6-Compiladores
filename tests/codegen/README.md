# Testes de Geração de Código (GCI)

Esta pasta documenta os casos de teste da **Pessoa 3** — geração e execução de scripts Python.

## Estrutura

- `data/` — datasets CSV sintéticos (50 linhas cada)
- `programs/` — programas `.mld` de entrada para codegen
- `output/` — scripts gerados e modelos `.pkl` (gitignored)

## Casos de teste

| Programa | Tipo | Modelo | Métricas | Resultado esperado |
|----------|------|--------|----------|-------------------|
| `programs/classification.mld` | Classificação | RandomForest | accuracy, f1_score | Script executa, imprime métricas, salva `.pkl` |
| `programs/regression.mld` | Regressão | LinearRegression | RMSE, MAE, R2 | Script executa, R² entre -1 e 1, salva `.pkl` |

## Como executar

Na raiz do projeto:

```bash
python -m pytest tests/test_codegen.py -q
```

Ou gerar manualmente:

```bash
python src/main/python/br/ufscar/dc/compiladores/mldeclara/main.py tests/codegen/programs/classification.mld > tests/codegen/output/generated_script.py
python tests/codegen/output/generated_script.py
```

## Decisões de design

- **Split treino/teste:** 80/20 fixo (`random_state=42`)
- **Variáveis categóricas:** codificação automática com `pd.get_dummies`
- **Múltiplos modelos:** cada bloco `MODEL` é treinado e avaliado; o último é serializado em `OUTPUT`
- **Mapeamento de classes:** RandomForest → `RandomForestClassifier`, XGBoost → `XGBClassifier`, etc.

# Tabela de Hiperparâmetros por Modelo

Esta página documenta quais hiperparâmetros são aceitos por cada algoritmo
suportado e os tipos/validações esperadas — usada pela análise semântica.

## Modelos e hiperparâmetros

- RandomForest
  - `n_estimators` : int (>= 1)
  - `max_depth`    : int (>= 1)
  - `random_state` : int

- XGBoost
  - `n_estimators` : int (>= 1)
  - `max_depth`    : int (>= 1)
  - `learning_rate`: float (> 0)

- LinearRegression
  - nenhum hiperparâmetro obrigatório (tabela vazia)

- LogisticRegression
  - `max_iter` : int (>= 1)
  - `C`        : float (> 0)

- SVM
  - `C`      : float (> 0)
  - `kernel` : str (ex.: "linear", "rbf")


## Observações
- Hiperparâmetros desconhecidos para um dado algoritmo são considerados erro semântico.
- A validação de tipos (int/float/str) e intervalos é realizada pela análise semântica.
- Esta tabela espelha o dicionário `modelo_para_hiperparams` em `semantic.py`.

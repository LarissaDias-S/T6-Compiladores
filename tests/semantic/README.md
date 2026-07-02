# Casos de Teste Semânticos — ML-Declara

Esta pasta documenta os casos de teste usados para validar a análise semântica da linguagem ML-Declara.

## Visão Geral
Os testes cobrem:
- presença e consistência de TARGET_VAR e FEATURES;
- validação de hiperparâmetros por algoritmo;
- compatibilidade entre modelo e métrica;
- detecção de features duplicadas;
- validação da extensão do arquivo em OUTPUT.

## Casos Implementados

### 1. Programa válido
- Entrada: um programa com DATASET, TARGET_VAR, FEATURES, um modelo RandomForest, métricas compatíveis e OUTPUT com extensão .pkl.
- Resultado esperado: programa aceito sem erros semânticos.

### 2. TARGET_VAR ausente no dataset
- Entrada: TARGET_VAR aponta para uma coluna que não está declarada em COLUMNS.
- Resultado esperado: erro semântico informando que a variável alvo não existe no dataset.

### 3. FEATURE não declarada no dataset
- Entrada: FEATURES inclui uma coluna que não está em COLUMNS.
- Resultado esperado: erro semântico informando que a feature não existe no dataset.

### 4. Hiperparâmetro inválido
- Entrada: um modelo recebe um hiperparâmetro com valor inválido, como max_depth = -2.
- Resultado esperado: erro semântico informando que o valor do hiperparâmetro é inválido.

### 5. Hiperparâmetro desconhecido
- Entrada: um modelo declara um hiperparâmetro que não é aceito para o algoritmo escolhido.
- Resultado esperado: erro semântico indicando que o hiperparâmetro não é válido para o modelo.

### 6. Métrica incompatível com o modelo
- Entrada: um modelo de regressão usa accuracy, ou um modelo de classificação usa RMSE.
- Resultado esperado: erro semântico de incompatibilidade modelo × métrica.

### 7. Features duplicadas
- Entrada: FEATURES repete o mesmo nome mais de uma vez.
- Resultado esperado: erro semântico informando duplicidade.

### 8. OUTPUT com extensão inválida
- Entrada: OUTPUT termina em .txt ou outro formato não suportado.
- Resultado esperado: erro semântico informando que a extensão deve ser .pkl ou .joblib.

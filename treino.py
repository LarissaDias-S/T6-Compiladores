"""
Script gerado automaticamente pelo compilador ML-Declara.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import LabelEncoder

# --- Carregamento do dataset ---
DATASET_PATH = 'dados/clientes.csv'
TARGET_VAR = 'comprou'
FEATURES = ['idade', 'salario', 'regiao']
OUTPUT_PATH = 'modelos/rf_clientes.pkl'

df = pd.read_csv(DATASET_PATH)

# --- PrÚ-processamento ---
X = df[FEATURES].copy()
y = df[TARGET_VAR].copy()

cat_cols = X.select_dtypes(include=['object', 'string', 'category']).columns.tolist()
if cat_cols:
    X = pd.get_dummies(X, columns=cat_cols, drop_first=False)

if y.dtype == 'object' or str(y.dtype) == 'string':
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

# --- DivisÒo treino/teste ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Modelo: classificador ---
classificador = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
classificador.fit(X_train, y_train)
y_pred_classificador = classificador.predict(X_test)

print('=== MÚtricas ù classificador (RandomForest) ===')
print(f'  accuracy: {accuracy_score(y_test, y_pred_classificador):.4f}')
print(f'  f1_score: {f1_score(y_test, y_pred_classificador, average="binary"):.4f}')

# --- SerializaþÒo do modelo ---
os.makedirs(os.path.dirname(OUTPUT_PATH) or '.', exist_ok=True)
joblib.dump(classificador, OUTPUT_PATH)
print(f'Modelo saved: {OUTPUT_PATH}')

"""
Script gerado automaticamente pelo compilador ML-Declara.
Treina o(s) modelo(s) declarado(s), avalia métricas e salva o artefato.
"""

import sys
import os
import joblib
import pandas as pd
import numpy as np
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.preprocessing import LabelEncoder

# --- Carregamento do dataset ---
DATASET_PATH = 'dados/fraude.csv'
TARGET_VAR = 'fraude'
FEATURES = ['valor', 'hora', 'tipo_transacao', 'pais']
OUTPUT_PATH = 'modelos/xgb_fraude.pkl'

df = pd.read_csv(DATASET_PATH)
missing_cols = set(FEATURES + [TARGET_VAR]) - set(df.columns)
if missing_cols:
    raise ValueError(f'Colunas ausentes no CSV: {sorted(missing_cols)}')

# --- Pré-processamento ---
# Separa features e alvo; codifica colunas categóricas com one-hot encoding
X = df[FEATURES].copy()
y = df[TARGET_VAR].copy()

cat_cols = X.select_dtypes(include=['object', 'string', 'category']).columns.tolist()
if cat_cols:
    X = pd.get_dummies(X, columns=cat_cols, drop_first=False)

# Codifica o alvo categórico para modelos de classificação
label_encoder = None
if y.dtype == 'object' or str(y.dtype) == 'string':
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

# --- Divisão treino/teste (80/20) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Modelo: detector_fraude (XGBoost) ---
detector_fraude = XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.1, random_state=0)
detector_fraude.fit(X_train, y_train)
y_pred_detector_fraude = detector_fraude.predict(X_test)

print('=== Métricas — detector_fraude (XGBoost) ===')
print(f'  accuracy: {accuracy_score(y_test, y_pred_detector_fraude):.4f}')
print(f'  f1_score: {f1_score(y_test, y_pred_detector_fraude, average="binary"):.4f}')
print(f'  precision: {precision_score(y_test, y_pred_detector_fraude, average="binary", zero_division=0):.4f}')
print(f'  recall: {recall_score(y_test, y_pred_detector_fraude, average="binary", zero_division=0):.4f}')

# --- Serialização do modelo ---
os.makedirs(os.path.dirname(OUTPUT_PATH) or '.', exist_ok=True)
joblib.dump(detector_fraude, OUTPUT_PATH)
print(f'Modelo salvo em: {OUTPUT_PATH}')

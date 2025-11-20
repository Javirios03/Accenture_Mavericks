import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

# -----------------------------
# 1. GENERAR 100 CLIENTES FAKE
# -----------------------------

np.random.seed(42)

n = 100  # número de clientes

ahorro_aportado = np.random.uniform(500, 5000, n)
financiacion_necesaria = np.random.uniform(1000, 10000, n)
valor_vivienda = ahorro_aportado + financiacion_necesaria + np.random.uniform(-2000, 2000, n)

data = {
    "ahorro_aportado": ahorro_aportado,
    "financiacion_necesaria": financiacion_necesaria,
    "valor_vivienda": valor_vivienda,
    "ltv": financiacion_necesaria / np.maximum(valor_vivienda, 1),
    "plazo_anios": np.random.choice([10, 15, 20, 25, 30], n),
    "ingresos_mensuales": np.random.uniform(1200, 6000, n),
    "gastos_mensuales": np.random.uniform(300, 2000, n),
    "dti": np.random.uniform(0.1, 0.6, n),
    "edad": np.random.randint(21, 70, n),
    "antiguedad_laboral": np.random.randint(0, 30, n),
    "credit_score": np.random.randint(350, 850, n),
}

df = pd.DataFrame(data)

# -----------------------------
# 2. OBJETIVO: interes_hipoteca
# -----------------------------

# Fórmula inventada para simular el tipo de interés
ruido = np.random.normal(0, 0.2, n)

df["interes_hipoteca"] = (
    1.5
    + df["ltv"] * 1.2
    + df["dti"] * 1.5
    + (700 - df["credit_score"]) * 0.002
    + ruido
).round(3)

# -----------------------------
# 3. SELECCIÓN DE FEATURES / TARGET
# -----------------------------

FEATURES = [
    "ahorro_aportado",
    "financiacion_necesaria",
    "valor_vivienda",
    "ltv",
    "plazo_anios",
    "ingresos_mensuales",
    "gastos_mensuales",
    "dti",
    "edad",
    "antiguedad_laboral",
    "credit_score",
]

TARGET = "interes_hipoteca"

X = df[FEATURES]
y = df[TARGET]

# -----------------------------
# 4. TRAIN / TEST = 80 / 20
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Nº total de clientes: {len(X)}")
print(f"Nº en train: {len(X_train)}")
print(f"Nº en test:  {len(X_test)}")

# -----------------------------
# 5. MODELO XGBOOST + SCALER
# -----------------------------

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        n_jobs=-1,
        tree_method="hist"
    ))
])

pipeline.fit(X_train, y_train)

# -----------------------------
# 6. EVALUACIÓN
# -----------------------------

y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nRESULTADOS DEL MODELO:")
print(f"MAE  = {mae:.4f}")
print(f"RMSE = {rmse:.4f}")

# -----------------------------
# 7. EJEMPLO DE PREDICCIÓN
# -----------------------------

ejemplo = X_test.iloc[0:1]
prediccion = pipeline.predict(ejemplo)[0]

print("\nEjemplo de cliente (test):")
print(ejemplo)

print(f"\nPredicción de interés hipotecario: {round(prediccion, 3)} %")

import matplotlib.pyplot as plt

# -----------------------------
# 8. FEATURE IMPORTANCE
# -----------------------------

# Sacamos el modelo XGBoost ya entrenado desde el pipeline
xgb_model = pipeline.named_steps["model"]

# Importancias de cada feature
importancias = xgb_model.feature_importances_

# Lo metemos en un DataFrame ordenado
fi_df = pd.DataFrame({
    "feature": FEATURES,
    "importance": importancias
}).sort_values("importance", ascending=False)

print("\nIMPORTANCIA DE FEATURES:")
print(fi_df)

# -----------------------------
# 9. GRÁFICA DE IMPORTANCIAS
# -----------------------------

plt.figure(figsize=(10, 6))
plt.bar(fi_df["feature"], fi_df["importance"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("Importancia")
plt.title("Importancia de cada feature en el modelo XGBoost")
plt.tight_layout()
plt.show()

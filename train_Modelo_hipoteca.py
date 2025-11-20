# clientes_a_diccionarios.py
from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor  # pip install xgboost

# ------------------ Mongo ------------------ #
uri = "mongodb+srv://gabriellazovsky_db_user:67PdWTyuQV8tlRYR@clustermaverick.cymy94z.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

def obtener_clientes():
    """Devuelve una lista de diccionarios con todos los clientes."""
    try:
        db = client["banco"]
        clientes = db["clientes"]
        lista_clientes = list(clientes.find({}, {"_id": 0}))
        return lista_clientes
    except Exception as e:
        print("Error al obtener clientes:", e)
        return []

# ------------------ Modelo ML ------------------ #

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

def entrenar_modelo(clientes_dicts):
    """
    Recibe lista de diccionarios (clientes) y devuelve un pipeline entrenado
    (StandardScaler + XGBRegressor).
    """
    df = pd.DataFrame(clientes_dicts)

    # Filtrar columnas necesarias
    df = df.dropna(subset=FEATURES + [TARGET])  # asegurarnos de que no hay NaN

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", XGBRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=4,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="reg:squarederror",
                n_jobs=-1,
                tree_method="hist",
            ))
        ]
    )

    pipeline.fit(X_train, y_train)

    # Evaluación rápida
    y_pred = pipeline.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"MAE en test (puntos de tipo de interés): {mae:.4f}")

    return pipeline

def answer_mortage(cliente_dict, modelo):
    x = [[cliente_dict[f] for f in FEATURES]]
    tipo_pred = modelo.predict(x)[0]
    return f"{round(float(tipo_pred), 3)} %"



if __name__ == "__main__":
    clientes = obtener_clientes()
    print(f"Clientes recuperados de Mongo: {len(clientes)}")

    modelo = entrenar_modelo(clientes)

    # Ejemplo: predecir el tipo para el primer cliente
    if clientes:
        ejemplo = clientes[0]
        tipo = answer_mortage(ejemplo, modelo)
        print("\nEjemplo de predicción para un cliente concreto:")
        print(ejemplo)
        print(f"Tipo de interés predicho: {tipo} %")

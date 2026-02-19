"""
utils.py
Funciones auxiliares para carga y preprocesamiento de datos.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def load_data(filepath: str) -> pd.DataFrame:
    """
    Carga el dataset desde un archivo CSV.
    
    Args:
        filepath: Ruta al archivo CSV.
    
    Returns:
        DataFrame con los datos cargados.
    """
    df = pd.read_csv(filepath)
    print(f"✓ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def prepare_features_target(df: pd.DataFrame, target_col: str = 'monto_mensual_ars'):
    """
    Separa variables explicativas (X) y objetivo (y).
    
    Args:
        df: DataFrame con los datos.
        target_col: Nombre de la columna objetivo.
    
    Returns:
        X (DataFrame), y (Series), numeric_features (list), categorical_features (list)
    """
    numeric_features = ['mes', 'superficie_m2', 'distancia_km', 'tecnico_id', 'servicios_mes']
    categorical_features = ['zona', 'tipo_cliente', 'tipo_servicio']
    features = numeric_features + categorical_features
    
    X = df[features]
    y = df[target_col]
    
    print(f"✓ Features (X): {X.shape[1]} columnas")
    print(f"✓ Target (y): {target_col}")
    
    return X, y, numeric_features, categorical_features


def split_data(X, y, test_size: float = 0.2, random_state: int = 42):
    """
    Divide los datos en entrenamiento y prueba.
    
    Args:
        X: Variables explicativas.
        y: Variable objetivo.
        test_size: Proporción del test set (default: 0.2).
        random_state: Semilla para reproducibilidad (default: 42).
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"✓ Train set: {X_train.shape[0]} muestras")
    print(f"✓ Test set: {X_test.shape[0]} muestras")
    return X_train, X_test, y_train, y_test


def build_preprocessor(numeric_features: list, categorical_features: list):
    """
    Construye el pipeline de preprocesamiento con ColumnTransformer.
    
    Args:
        numeric_features: Lista de nombres de columnas numéricas.
        categorical_features: Lista de nombres de columnas categóricas.
    
    Returns:
        ColumnTransformer configurado.
    """
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    print("✓ Preprocessor configurado: StandardScaler + OneHotEncoder")
    return preprocessor
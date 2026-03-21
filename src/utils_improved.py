"""
utils_improved.py
Funciones auxiliares mejoradas para carga, preparación y partición de datos
en la PoC analítica del TFG Leplag.
"""

from __future__ import annotations

from typing import Optional, Tuple, List

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GroupShuffleSplit, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class DataPreparationError(Exception):
    """Error de preparación de datos para el pipeline analítico."""


DEFAULT_TARGET = "monto_mensual_ars"
GROUP_COLUMN = "id_cliente_anon"


def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    print(f"✓ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def prepare_model_inputs(
    df: pd.DataFrame,
    target_col: str = DEFAULT_TARGET,
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str], Optional[pd.Series]]:
    if target_col not in df.columns:
        raise DataPreparationError(f"No se encontró la columna objetivo: {target_col}")

    numeric_features = ["mes", "superficie_m2", "distancia_km", "servicios_mes"]
    categorical_features = ["zona", "tipo_cliente", "tipo_servicio"]

    if "tecnico_id" in df.columns:
        categorical_features.append("tecnico_id")

    feature_cols = numeric_features + categorical_features
    missing = [col for col in feature_cols if col not in df.columns]
    if missing:
        raise DataPreparationError(f"Faltan columnas requeridas para el modelo: {missing}")

    X = df[feature_cols].copy()
    y = df[target_col].copy()
    groups = df[GROUP_COLUMN].copy() if GROUP_COLUMN in df.columns else None

    print(f"✓ Features numéricas: {numeric_features}")
    print(f"✓ Features categóricas: {categorical_features}")
    print(f"✓ Target (y): {target_col}")
    print(f"✓ Uso de agrupación por cliente: {groups is not None}")

    return X, y, numeric_features, categorical_features, groups


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    groups: Optional[pd.Series] = None,
    test_size: float = 0.2,
    random_state: int = 42,
):
    if groups is not None:
        splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
        train_idx, test_idx = next(splitter.split(X, y, groups=groups))

        X_train = X.iloc[train_idx].copy()
        X_test = X.iloc[test_idx].copy()
        y_train = y.iloc[train_idx].copy()
        y_test = y.iloc[test_idx].copy()
        groups_train = groups.iloc[train_idx].copy()
        groups_test = groups.iloc[test_idx].copy()

        print(f"✓ Train set: {X_train.shape[0]} muestras")
        print(f"✓ Test set: {X_test.shape[0]} muestras")
        print(f"✓ Clientes únicos en train: {groups_train.nunique()}")
        print(f"✓ Clientes únicos en test: {groups_test.nunique()}")
        print("✓ Split agrupado por cliente aplicado")

        return X_train, X_test, y_train, y_test, groups_train, groups_test

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(f"✓ Train set: {X_train.shape[0]} muestras")
    print(f"✓ Test set: {X_test.shape[0]} muestras")
    print("✓ Split aleatorio estándar aplicado")

    return X_train, X_test, y_train, y_test, None, None


def build_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    print("✓ Preprocessor configurado: imputación + StandardScaler + OneHotEncoder")
    return preprocessor

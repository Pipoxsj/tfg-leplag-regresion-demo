"""
loaders.py

Carga inicial de fuentes sanitizadas del prototipo de integración,
trazabilidad y analítica complementaria a FusionWEB.

Fuentes esperadas en data/raw/:
- clientes_fusionweb.csv
- servicios_u_ot_fusionweb.csv
- tecnicos_complementario.csv

Esta versión prioriza:
1. lectura robusta de CSV,
2. estandarización básica de nombres de columnas,
3. limpieza mínima de texto,
4. validación de columnas requeridas,
5. trazabilidad simple por consola.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

# Raíz del proyecto: src/ingest/loaders.py -> ../../
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


class LoaderError(Exception):
    """Error de carga o validación de fuentes."""


EXPECTED_FILES = {
    "clientes": RAW_DIR / "clientes_fusionweb.csv",
    "servicios": RAW_DIR / "servicios_u_ot_fusionweb.csv",
    "tecnicos": RAW_DIR / "tecnicos_complementario.csv",
}


REQUIRED_COLUMNS = {
    "clientes": ["cliente_numero", "cliente_id", "direccion_id"],
    "servicios": [
        "horario",
        "origen",
        "estado_servicio",
        "tecnico_id",
        "cliente_id",
        "sucursal_id",
        "direccion_id",
        "servicios",
    ],
    "tecnicos": ["tecnico_id", "tecnico_nombre", "activo", "fuente"],
}


def standardize_column_name(name: str) -> str:
    """Estandariza nombres de columnas para facilitar validación y joins."""
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
    )



def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [standardize_column_name(col) for col in df.columns]
    return df



def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza mínima de campos string sin forzar catálogos todavía."""
    df = df.copy()
    object_cols = df.select_dtypes(include=["object", "string"]).columns

    for col in object_cols:
        df[col] = (
            df[col]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    return df



def read_csv_safe(path: Path, sep: str = ",") -> pd.DataFrame:
    """Lee un CSV con configuración tolerante a archivos operativos."""
    if not path.exists():
        raise LoaderError(f"No se encontró el archivo esperado: {path}")

    try:
        df = pd.read_csv(path, sep=sep, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, sep=sep, encoding="latin-1")
    except Exception as exc:
        raise LoaderError(f"Error al leer {path.name}: {exc}") from exc

    return df



def validate_required_columns(df: pd.DataFrame, source_name: str) -> None:
    required = REQUIRED_COLUMNS[source_name]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise LoaderError(
            f"La fuente '{source_name}' no contiene las columnas requeridas: {missing}"
        )



def log_load_summary(df: pd.DataFrame, source_name: str) -> None:
    print(
        f"[LOAD OK] {source_name}: filas={len(df)}, columnas={len(df.columns)} -> {list(df.columns)}"
    )



def base_load(path: Path, source_name: str) -> pd.DataFrame:
    df = read_csv_safe(path)
    df = standardize_columns(df)
    df = clean_text_columns(df)
    validate_required_columns(df, source_name)
    log_load_summary(df, source_name)
    return df



def load_clientes(path: Path | None = None) -> pd.DataFrame:
    """Carga la dimensión de clientes."""
    path = path or EXPECTED_FILES["clientes"]
    df = base_load(path, "clientes")

    # Conversión liviana de tipos
    if "cliente_numero" in df.columns:
        df["cliente_numero"] = pd.to_numeric(df["cliente_numero"], errors="coerce")

    return df



def load_servicios(path: Path | None = None) -> pd.DataFrame:
    """Carga la tabla base de órdenes de trabajo / servicios."""
    path = path or EXPECTED_FILES["servicios"]
    df = base_load(path, "servicios")

    # Genera un identificador técnico si aún no existe uno estable
    if "servicio_id" not in df.columns:
        df.insert(0, "servicio_id", [f"SERV-{i+1:04d}" for i in range(len(df))])

    # Normalización liviana de estados
    if "estado_servicio" in df.columns:
        df["estado_servicio"] = df["estado_servicio"].str.upper()

    return df



def load_tecnicos(path: Path | None = None) -> pd.DataFrame:
    """Carga la dimensión de técnicos."""
    path = path or EXPECTED_FILES["tecnicos"]
    df = base_load(path, "tecnicos")

    if "activo" in df.columns:
        df["activo"] = (
            df["activo"]
            .astype("string")
            .str.upper()
            .map({"TRUE": True, "FALSE": False})
            .fillna(False)
        )

    return df



def load_all_sources() -> Dict[str, pd.DataFrame]:
    """Carga todas las fuentes mínimas del prototipo."""
    return {
        "clientes": load_clientes(),
        "servicios": load_servicios(),
        "tecnicos": load_tecnicos(),
    }



def print_basic_diagnostics(dataframes: Dict[str, pd.DataFrame]) -> None:
    """Muestra diagnósticos rápidos para verificar consistencia inicial."""
    print("\n=== DIAGNÓSTICO BÁSICO DE FUENTES ===")
    for name, df in dataframes.items():
        print(f"\nFuente: {name}")
        print(f"- Filas: {len(df)}")
        print(f"- Columnas: {len(df.columns)}")
        print(f"- Nulos por columna:")
        print(df.isna().sum())



def validate_cross_source_consistency(
    clientes: pd.DataFrame,
    servicios: pd.DataFrame,
    tecnicos: pd.DataFrame,
) -> None:
    """Chequeos mínimos entre tablas para detectar inconsistencias tempranas."""
    print("\n=== VALIDACIÓN CRUZADA BÁSICA ===")

    client_ids_in_servicios = set(servicios["cliente_id"].dropna().unique())
    client_ids_master = set(clientes["cliente_id"].dropna().unique())
    missing_client_ids = sorted(client_ids_in_servicios - client_ids_master)
    print(f"- Clientes referenciados en servicios y ausentes en clientes: {len(missing_client_ids)}")
    if missing_client_ids[:10]:
        print(f"  Ejemplos: {missing_client_ids[:10]}")

    tecnico_ids_in_servicios = set(servicios["tecnico_id"].dropna().unique())
    tecnico_ids_master = set(tecnicos["tecnico_id"].dropna().unique())
    missing_tecnico_ids = sorted(tecnico_ids_in_servicios - tecnico_ids_master)
    print(f"- Técnicos referenciados en servicios y ausentes en técnicos: {len(missing_tecnico_ids)}")
    if missing_tecnico_ids[:10]:
        print(f"  Ejemplos: {missing_tecnico_ids[:10]}")



def run_initial_load() -> Dict[str, pd.DataFrame]:
    """Pipeline mínimo de carga para pruebas rápidas desde consola."""
    dataframes = load_all_sources()
    print_basic_diagnostics(dataframes)
    validate_cross_source_consistency(
        clientes=dataframes["clientes"],
        servicios=dataframes["servicios"],
        tecnicos=dataframes["tecnicos"],
    )
    return dataframes


if __name__ == "__main__":
    run_initial_load()

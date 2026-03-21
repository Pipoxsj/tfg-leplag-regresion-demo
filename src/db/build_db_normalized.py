"""
build_db_normalized.py

Versión extendida del builder DuckDB para el prototipo de Leplag.
Además de cargar clientes, servicios y técnicos, incorpora una tabla
normalizada de tipos de servicio a partir del campo compuesto `servicios`.

Uso recomendado desde la raíz del repo:
    python -m src.db.build_db_normalized
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from src.ingest.loaders import run_initial_load
from src.transform.normalize import normalize_servicios_tipos, summarize_normalized_types

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROCESSED_DIR / "leplag.duckdb"


def ensure_directories() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_sources() -> dict[str, pd.DataFrame]:
    return run_initial_load()


def create_base_tables(con: duckdb.DuckDBPyConnection, dataframes: dict[str, pd.DataFrame]) -> pd.DataFrame:
    clientes = dataframes["clientes"].copy()
    servicios = dataframes["servicios"].copy()
    tecnicos = dataframes["tecnicos"].copy()
    servicios_tipos = normalize_servicios_tipos(servicios)

    con.register("clientes_df", clientes)
    con.register("servicios_df", servicios)
    con.register("tecnicos_df", tecnicos)
    con.register("servicios_tipos_df", servicios_tipos)

    con.execute("DROP TABLE IF EXISTS clientes")
    con.execute("DROP TABLE IF EXISTS servicios")
    con.execute("DROP TABLE IF EXISTS tecnicos")
    con.execute("DROP TABLE IF EXISTS servicios_tipos")

    con.execute("CREATE TABLE clientes AS SELECT * FROM clientes_df")
    con.execute("CREATE TABLE servicios AS SELECT * FROM servicios_df")
    con.execute("CREATE TABLE tecnicos AS SELECT * FROM tecnicos_df")
    con.execute("CREATE TABLE servicios_tipos AS SELECT * FROM servicios_tipos_df")

    return servicios_tipos


def create_views(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("DROP VIEW IF EXISTS vw_trazabilidad_servicios")
    con.execute("DROP VIEW IF EXISTS vw_trazabilidad_servicios_tipos")

    con.execute(
        """
        CREATE VIEW vw_trazabilidad_servicios AS
        SELECT
            s.servicio_id,
            s.horario,
            s.origen,
            s.estado_servicio,
            s.cliente_id,
            c.cliente_numero,
            c.direccion_id AS cliente_direccion_id,
            s.sucursal_id,
            s.direccion_id AS servicio_direccion_id,
            s.tecnico_id,
            t.tecnico_nombre,
            t.activo AS tecnico_activo,
            s.servicios,
            s.consumo,
            CASE WHEN c.cliente_id IS NULL THEN TRUE ELSE FALSE END AS cliente_faltante,
            CASE WHEN t.tecnico_id IS NULL THEN TRUE ELSE FALSE END AS tecnico_faltante
        FROM servicios s
        LEFT JOIN clientes c ON s.cliente_id = c.cliente_id
        LEFT JOIN tecnicos t ON s.tecnico_id = t.tecnico_id
        """
    )

    con.execute(
        """
        CREATE VIEW vw_trazabilidad_servicios_tipos AS
        SELECT
            v.servicio_id,
            v.horario,
            v.origen,
            v.estado_servicio,
            v.cliente_id,
            v.cliente_numero,
            v.sucursal_id,
            v.servicio_direccion_id,
            v.tecnico_id,
            v.tecnico_nombre,
            st.servicio_tipo,
            st.tipo_ordinal,
            st.cantidad_tipos_en_servicio
        FROM vw_trazabilidad_servicios v
        LEFT JOIN servicios_tipos st ON v.servicio_id = st.servicio_id
        """
    )


def run_checks(con: duckdb.DuckDBPyConnection, servicios_tipos_df: pd.DataFrame) -> None:
    print("\n=== VERIFICACIÓN BASE DUCKDB NORMALIZADA ===")

    clientes_count = con.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    servicios_count = con.execute("SELECT COUNT(*) FROM servicios").fetchone()[0]
    tecnicos_count = con.execute("SELECT COUNT(*) FROM tecnicos").fetchone()[0]
    servicios_tipos_count = con.execute("SELECT COUNT(*) FROM servicios_tipos").fetchone()[0]
    trazabilidad_count = con.execute("SELECT COUNT(*) FROM vw_trazabilidad_servicios").fetchone()[0]
    trazabilidad_tipos_count = con.execute("SELECT COUNT(*) FROM vw_trazabilidad_servicios_tipos").fetchone()[0]

    print(f"- clientes: {clientes_count}")
    print(f"- servicios: {servicios_count}")
    print(f"- tecnicos: {tecnicos_count}")
    print(f"- servicios_tipos: {servicios_tipos_count}")
    print(f"- vw_trazabilidad_servicios: {trazabilidad_count}")
    print(f"- vw_trazabilidad_servicios_tipos: {trazabilidad_tipos_count}")

    resumen_estados = con.execute(
        """
        SELECT estado_servicio, COUNT(*) AS cantidad
        FROM vw_trazabilidad_servicios
        GROUP BY estado_servicio
        ORDER BY cantidad DESC, estado_servicio
        """
    ).fetchdf()

    print("\n=== RESUMEN POR ESTADO DE SERVICIO ===")
    print(resumen_estados)

    resumen_tipos = summarize_normalized_types(servicios_tipos_df)
    print("\n=== RESUMEN DE TIPOS DE SERVICIO NORMALIZADOS ===")
    print(resumen_tipos)


def main() -> None:
    print("=" * 70)
    print("CONSTRUCCIÓN DE BASE DUCKDB NORMALIZADA - PROTOTIPO LEPLAG")
    print("=" * 70)

    ensure_directories()
    dataframes = load_sources()

    con = duckdb.connect(str(DB_PATH))
    try:
        servicios_tipos_df = create_base_tables(con, dataframes)
        create_views(con)
        run_checks(con, servicios_tipos_df)
    finally:
        con.close()

    print("\n" + "=" * 70)
    print(f"BASE NORMALIZADA GENERADA CORRECTAMENTE EN: {DB_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()

"""
build_db.py

Construye una base DuckDB local para el prototipo de integración,
trazabilidad y analítica complementaria a FusionWEB.

Qué hace esta versión:
1. carga clientes, servicios y técnicos desde src.ingest.loaders,
2. crea la base data/processed/leplag.duckdb,
3. persiste tablas base,
4. crea una vista inicial de trazabilidad,
5. imprime verificaciones simples por consola.

Uso recomendado desde la raíz del repo:
    python -m src.db.build_db
"""

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd

from src.ingest.loaders import run_initial_load

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROCESSED_DIR / "leplag.duckdb"


def ensure_directories() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_sources() -> dict[str, pd.DataFrame]:
    return run_initial_load()


def create_base_tables(con: duckdb.DuckDBPyConnection, dataframes: dict[str, pd.DataFrame]) -> None:
    clientes = dataframes["clientes"].copy()
    servicios = dataframes["servicios"].copy()
    tecnicos = dataframes["tecnicos"].copy()

    con.register("clientes_df", clientes)
    con.register("servicios_df", servicios)
    con.register("tecnicos_df", tecnicos)

    con.execute("DROP TABLE IF EXISTS clientes")
    con.execute("DROP TABLE IF EXISTS servicios")
    con.execute("DROP TABLE IF EXISTS tecnicos")

    con.execute("CREATE TABLE clientes AS SELECT * FROM clientes_df")
    con.execute("CREATE TABLE servicios AS SELECT * FROM servicios_df")
    con.execute("CREATE TABLE tecnicos AS SELECT * FROM tecnicos_df")


def create_views(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("DROP VIEW IF EXISTS vw_trazabilidad_servicios")

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
            CASE
                WHEN c.cliente_id IS NULL THEN TRUE
                ELSE FALSE
            END AS cliente_faltante,
            CASE
                WHEN t.tecnico_id IS NULL THEN TRUE
                ELSE FALSE
            END AS tecnico_faltante
        FROM servicios s
        LEFT JOIN clientes c
            ON s.cliente_id = c.cliente_id
        LEFT JOIN tecnicos t
            ON s.tecnico_id = t.tecnico_id
        """
    )


def run_checks(con: duckdb.DuckDBPyConnection) -> None:
    print("\n=== VERIFICACIÓN BASE DUCKDB ===")

    clientes_count = con.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
    servicios_count = con.execute("SELECT COUNT(*) FROM servicios").fetchone()[0]
    tecnicos_count = con.execute("SELECT COUNT(*) FROM tecnicos").fetchone()[0]
    trazabilidad_count = con.execute("SELECT COUNT(*) FROM vw_trazabilidad_servicios").fetchone()[0]

    print(f"- clientes: {clientes_count}")
    print(f"- servicios: {servicios_count}")
    print(f"- tecnicos: {tecnicos_count}")
    print(f"- vw_trazabilidad_servicios: {trazabilidad_count}")

    resumen = con.execute(
        """
        SELECT
            estado_servicio,
            COUNT(*) AS cantidad
        FROM vw_trazabilidad_servicios
        GROUP BY estado_servicio
        ORDER BY cantidad DESC, estado_servicio
        """
    ).fetchdf()

    print("\n=== RESUMEN POR ESTADO DE SERVICIO ===")
    print(resumen)

    faltantes = con.execute(
        """
        SELECT
            SUM(CASE WHEN cliente_faltante THEN 1 ELSE 0 END) AS clientes_faltantes,
            SUM(CASE WHEN tecnico_faltante THEN 1 ELSE 0 END) AS tecnicos_faltantes
        FROM vw_trazabilidad_servicios
        """
    ).fetchdf()

    print("\n=== FALTANTES EN TRAZABILIDAD ===")
    print(faltantes)


def main() -> None:
    print("=" * 70)
    print("CONSTRUCCIÓN DE BASE DUCKDB - PROTOTIPO LEPLAG")
    print("=" * 70)

    ensure_directories()
    dataframes = load_sources()

    con = duckdb.connect(str(DB_PATH))
    try:
        create_base_tables(con, dataframes)
        create_views(con)
        run_checks(con)
    finally:
        con.close()

    print("\n" + "=" * 70)
    print(f"BASE GENERADA CORRECTAMENTE EN: {DB_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    main()

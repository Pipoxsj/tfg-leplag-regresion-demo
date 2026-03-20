"""
run_ingest.py

Punto de entrada mínimo para ejecutar la carga inicial de fuentes
sanitizadas del prototipo.

Uso recomendado desde la raíz del repositorio:
    python src/ingest/run_ingest.py
"""

from __future__ import annotations

from src.ingest.loaders import LoaderError, run_initial_load


def main() -> None:
    print("=" * 70)
    print("INICIO DE CARGA - PROTOTIPO LEPLAG")
    print("=" * 70)

    try:
        dataframes = run_initial_load()
        print("\n" + "=" * 70)
        print("CARGA FINALIZADA CORRECTAMENTE")
        print("=" * 70)
        print("\nResumen de fuentes cargadas:")
        for name, df in dataframes.items():
            print(f"- {name}: {len(df)} filas, {len(df.columns)} columnas")

    except LoaderError as exc:
        print("\n" + "=" * 70)
        print("ERROR DE CARGA")
        print("=" * 70)
        print(str(exc))
        raise SystemExit(1)

    except Exception as exc:
        print("\n" + "=" * 70)
        print("ERROR INESPERADO")
        print("=" * 70)
        print(str(exc))
        raise SystemExit(2)


if __name__ == "__main__":
    main()

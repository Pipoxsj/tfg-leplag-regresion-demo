from pathlib import Path

import duckdb
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / 'data' / 'processed' / 'leplag.duckdb'


def load_summary_data():
    if not DB_PATH.exists():
        raise FileNotFoundError('No se encontró la base DuckDB. Ejecuta primero: python -m src.db.build_db_normalized')

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        resumen_tablas = con.execute(
            """
            SELECT 'clientes' AS tabla, COUNT(*) AS cantidad FROM clientes
            UNION ALL
            SELECT 'servicios' AS tabla, COUNT(*) AS cantidad FROM servicios
            UNION ALL
            SELECT 'tecnicos' AS tabla, COUNT(*) AS cantidad FROM tecnicos
            UNION ALL
            SELECT 'servicios_tipos' AS tabla, COUNT(*) AS cantidad FROM servicios_tipos
            """
        ).fetchdf()

        estados = con.execute(
            """
            SELECT estado_servicio, COUNT(*) AS cantidad
            FROM vw_trazabilidad_servicios
            GROUP BY estado_servicio
            ORDER BY cantidad DESC, estado_servicio
            """
        ).fetchdf()

        tipos = con.execute(
            """
            SELECT servicio_tipo, COUNT(*) AS cantidad
            FROM servicios_tipos
            GROUP BY servicio_tipo
            ORDER BY cantidad DESC, servicio_tipo
            """
        ).fetchdf()

        trazabilidad = con.execute(
            """
            SELECT *
            FROM vw_trazabilidad_servicios
            ORDER BY servicio_id
            LIMIT 20
            """
        ).fetchdf()
    finally:
        con.close()

    return resumen_tablas, estados, tipos, trazabilidad


def main():
    st.title('Prototipo Leplag - Integración, trazabilidad y analítica')
    st.write('Capa funcional complementaria a FusionWEB, basada en fuentes sanitizadas y base DuckDB local.')

    try:
        resumen_tablas, estados, tipos, trazabilidad = load_summary_data()
    except Exception as exc:
        st.error(str(exc))
        return

    st.subheader('Resumen de tablas')
    st.dataframe(resumen_tablas)

    st.subheader('Servicios por estado')
    st.dataframe(estados)

    st.subheader('Tipos de servicio normalizados')
    st.dataframe(tipos)

    st.subheader('Muestra de trazabilidad')
    st.dataframe(trazabilidad)

    st.write('Siguiente paso recomendado: agregar páginas de trazabilidad detallada y dashboard operativo.')


if __name__ == '__main__':
    main()

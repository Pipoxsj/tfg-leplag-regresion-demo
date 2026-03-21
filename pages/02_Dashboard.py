from pathlib import Path

import duckdb
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / 'data' / 'processed' / 'leplag.duckdb'


def load_dashboard_data():
    if not DB_PATH.exists():
        raise FileNotFoundError('No se encontró la base DuckDB. Ejecuta primero: python -m src.db.build_db_normalized')

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        kpis = con.execute(
            """
            SELECT
                COUNT(*) AS servicios_total,
                SUM(CASE WHEN estado_servicio = 'FINALIZADO' THEN 1 ELSE 0 END) AS servicios_finalizados,
                SUM(CASE WHEN estado_servicio = 'PENDIENTE' THEN 1 ELSE 0 END) AS servicios_pendientes,
                COUNT(DISTINCT tecnico_id) AS tecnicos_con_servicios
            FROM vw_trazabilidad_servicios
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

        por_tecnico = con.execute(
            """
            SELECT tecnico_id, tecnico_nombre, COUNT(*) AS cantidad
            FROM vw_trazabilidad_servicios
            GROUP BY tecnico_id, tecnico_nombre
            ORDER BY cantidad DESC, tecnico_id
            """
        ).fetchdf()

        por_tipo = con.execute(
            """
            SELECT servicio_tipo, COUNT(*) AS cantidad
            FROM servicios_tipos
            GROUP BY servicio_tipo
            ORDER BY cantidad DESC, servicio_tipo
            """
        ).fetchdf()
    finally:
        con.close()

    return kpis, estados, por_tecnico, por_tipo


def main():
    st.title('Dashboard operativo')
    st.write('Indicadores básicos del prototipo Leplag sobre la base DuckDB local.')

    try:
        kpis, estados, por_tecnico, por_tipo = load_dashboard_data()
    except Exception as exc:
        st.error(str(exc))
        return

    fila = kpis.iloc[0]
    st.subheader('KPIs principales')
    st.write('Servicios totales:', int(fila['servicios_total']))
    st.write('Servicios finalizados:', int(fila['servicios_finalizados']))
    st.write('Servicios pendientes:', int(fila['servicios_pendientes']))
    st.write('Técnicos con servicios:', int(fila['tecnicos_con_servicios']))

    st.subheader('Servicios por estado')
    st.dataframe(estados)

    st.subheader('Servicios por técnico')
    st.dataframe(por_tecnico)

    st.subheader('Tipos de servicio normalizados')
    st.dataframe(por_tipo)

    st.write('Esta página resume el comportamiento operativo básico del prototipo.')


if __name__ == '__main__':
    main()

from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / 'data' / 'processed' / 'leplag.duckdb'


@st.cache_data
def load_summary_data() -> dict[str, pd.DataFrame]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f'No se encontró la base DuckDB en: {DB_PATH}')

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

    return {
        'resumen_tablas': resumen_tablas,
        'estados': estados,
        'tipos': tipos,
        'trazabilidad': trazabilidad,
    }


def main() -> None:
    st.set_page_config(page_title='Prototipo Leplag', layout='wide')

    st.title('Prototipo Leplag - Integración, trazabilidad y analítica')
    st.caption('Capa funcional complementaria a FusionWEB, basada en fuentes sanitizadas y base DuckDB local.')

    try:
        data = load_summary_data()
    except Exception as exc:
        st.error(f'No se pudo cargar la base del prototipo: {exc}')
        st.info('Antes de abrir esta app, ejecuta: python -m src.db.build_db_normalized')
        return

    resumen_tablas = data['resumen_tablas']
    estados = data['estados']
    tipos = data['tipos']
    trazabilidad = data['trazabilidad']

    c1, c2, c3, c4 = st.columns(4)
    resumen_dict = {row['tabla']: int(row['cantidad']) for _, row in resumen_tablas.iterrows()}
    c1.metric('Clientes', resumen_dict.get('clientes', 0))
    c2.metric('Servicios', resumen_dict.get('servicios', 0))
    c3.metric('Técnicos', resumen_dict.get('tecnicos', 0))
    c4.metric('Servicios normalizados', resumen_dict.get('servicios_tipos', 0))

    st.subheader('Resumen de tablas')
    st.dataframe(resumen_tablas, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader('Servicios por estado')
        st.dataframe(estados, use_container_width=True)
    with col_b:
        st.subheader('Tipos de servicio normalizados')
        st.dataframe(tipos, use_container_width=True)

    st.subheader('Muestra de trazabilidad')
    st.dataframe(trazabilidad, use_container_width=True)

    st.info('Siguiente paso recomendado: agregar páginas de trazabilidad detallada y dashboard operativo.')


if __name__ == '__main__':
    main()

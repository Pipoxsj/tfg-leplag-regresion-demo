from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / 'data' / 'processed' / 'leplag.duckdb'


def load_trazabilidad():
    if not DB_PATH.exists():
        raise FileNotFoundError('No se encontró la base DuckDB. Ejecuta primero: python -m src.db.build_db_normalized')

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        df = con.execute(
            """
            SELECT
                servicio_id,
                horario,
                origen,
                estado_servicio,
                cliente_id,
                cliente_numero,
                sucursal_id,
                servicio_direccion_id,
                tecnico_id,
                tecnico_nombre,
                servicios,
                consumo,
                cliente_faltante,
                tecnico_faltante
            FROM vw_trazabilidad_servicios
            ORDER BY servicio_id
            """
        ).fetchdf()

        tipos_df = con.execute(
            """
            SELECT
                servicio_id,
                servicio_tipo,
                tipo_ordinal,
                cantidad_tipos_en_servicio
            FROM servicios_tipos
            ORDER BY servicio_id, tipo_ordinal
            """
        ).fetchdf()
    finally:
        con.close()

    return df, tipos_df


def apply_filters(df, servicio_id, cliente_id, tecnico_id, estado_servicio):
    filtered = df.copy()

    if servicio_id != 'Todos':
        filtered = filtered[filtered['servicio_id'] == servicio_id]
    if cliente_id != 'Todos':
        filtered = filtered[filtered['cliente_id'] == cliente_id]
    if tecnico_id != 'Todos':
        filtered = filtered[filtered['tecnico_id'] == tecnico_id]
    if estado_servicio != 'Todos':
        filtered = filtered[filtered['estado_servicio'] == estado_servicio]

    return filtered


def main():
    st.title('Trazabilidad de servicios')
    st.write('Consulta detallada de servicios integrados desde la base DuckDB del prototipo.')

    try:
        trazabilidad_df, tipos_df = load_trazabilidad()
    except Exception as exc:
        st.error(str(exc))
        return

    servicio_options = ['Todos'] + sorted(trazabilidad_df['servicio_id'].dropna().astype(str).unique().tolist())
    cliente_options = ['Todos'] + sorted(trazabilidad_df['cliente_id'].dropna().astype(str).unique().tolist())
    tecnico_options = ['Todos'] + sorted(trazabilidad_df['tecnico_id'].dropna().astype(str).unique().tolist())
    estado_options = ['Todos'] + sorted(trazabilidad_df['estado_servicio'].dropna().astype(str).unique().tolist())

    st.subheader('Filtros')
    servicio_id = st.selectbox('Servicio', servicio_options)
    cliente_id = st.selectbox('Cliente', cliente_options)
    tecnico_id = st.selectbox('Técnico', tecnico_options)
    estado_servicio = st.selectbox('Estado', estado_options)

    filtered = apply_filters(trazabilidad_df, servicio_id, cliente_id, tecnico_id, estado_servicio)

    st.subheader('Resultados de trazabilidad')
    st.write('Cantidad de registros:', len(filtered))
    st.dataframe(filtered)

    if len(filtered) > 0:
        selected_service = filtered.iloc[0]['servicio_id']
        st.subheader('Ficha del primer servicio filtrado')
        ficha = filtered.iloc[0]
        st.write('Servicio ID:', ficha['servicio_id'])
        st.write('Cliente ID:', ficha['cliente_id'])
        st.write('Cliente número:', ficha['cliente_numero'])
        st.write('Técnico ID:', ficha['tecnico_id'])
        st.write('Técnico nombre:', ficha['tecnico_nombre'])
        st.write('Estado:', ficha['estado_servicio'])
        st.write('Horario:', ficha['horario'])
        st.write('Origen:', ficha['origen'])
        st.write('Servicios originales:', ficha['servicios'])
        st.write('Consumo:', ficha['consumo'])

        st.subheader('Tipos normalizados del servicio seleccionado')
        tipos_selected = tipos_df[tipos_df['servicio_id'] == selected_service]
        st.dataframe(tipos_selected)

    st.write('Esta página permite demostrar trazabilidad básica y normalización de tipos de servicio.')


if __name__ == '__main__':
    main()

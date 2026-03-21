from __future__ import annotations

from typing import List
import pandas as pd


class NormalizeError(Exception):
    pass


def clean_service_type(value: str) -> str:
    text = str(value).strip().upper()
    text = text.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    text = ' '.join(text.split())
    return text


def split_service_types(value: str) -> List[str]:
    if pd.isna(value):
        return []
    raw = str(value)
    parts = [clean_service_type(p) for p in raw.split(',')]
    parts = [p for p in parts if p]
    deduped = []
    for p in parts:
        if p not in deduped:
            deduped.append(p)
    return deduped


def normalize_servicios_tipos(servicios_df: pd.DataFrame) -> pd.DataFrame:
    required = {'servicio_id', 'servicios'}
    if not required.issubset(servicios_df.columns):
        raise NormalizeError(f'Faltan columnas requeridas: {required - set(servicios_df.columns)}')

    rows = []
    for _, row in servicios_df.iterrows():
        servicio_id = row['servicio_id']
        tipos = split_service_types(row['servicios'])

        if not tipos:
            rows.append({
                'servicio_id': servicio_id,
                'servicio_tipo': None,
                'tipo_ordinal': 1,
                'cantidad_tipos_en_servicio': 0,
            })
            continue

        for idx, tipo in enumerate(tipos, start=1):
            rows.append({
                'servicio_id': servicio_id,
                'servicio_tipo': tipo,
                'tipo_ordinal': idx,
                'cantidad_tipos_en_servicio': len(tipos),
            })

    return pd.DataFrame(rows)


def summarize_normalized_types(servicios_tipos_df: pd.DataFrame) -> pd.DataFrame:
    if servicios_tipos_df.empty:
        return pd.DataFrame(columns=['servicio_tipo', 'cantidad'])

    return (
        servicios_tipos_df.groupby('servicio_tipo', dropna=False, as_index=False)
        .size()
        .rename(columns={'size': 'cantidad'})
        .sort_values(by=['cantidad', 'servicio_tipo'], ascending=[False, True])
        .reset_index(drop=True)
    )

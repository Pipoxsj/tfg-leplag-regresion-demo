from __future__ import annotations

from typing import Dict, List
import pandas as pd

VALID_SERVICE_STATUSES = {"FINALIZADO", "PENDIENTE"}


class QualityRuleError(Exception):
    pass


def _issue(rule_id: str, severity: str, entity_type: str, entity_id: str, issue_type: str, issue_description: str, source_table: str) -> dict:
    return {
        "rule_id": rule_id,
        "severity": severity,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "issue_type": issue_type,
        "issue_description": issue_description,
        "source_table": source_table,
    }


def evaluate_quality_rules(dataframes: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    if not {"clientes", "servicios", "tecnicos"}.issubset(dataframes.keys()):
        raise QualityRuleError("Missing required tables.")

    servicios = dataframes["servicios"].copy()
    tecnicos = dataframes["tecnicos"][['tecnico_id', 'activo']].copy()

    issues: List[dict] = []

    for _, row in servicios.loc[servicios['cliente_id'].isna() | (servicios['cliente_id'].astype('string').str.strip() == ''), ['servicio_id']].iterrows():
        issues.append(_issue('R001', 'ALTA', 'servicio', str(row['servicio_id']), 'servicio_sin_cliente', 'El servicio no posee cliente_id asociado.', 'servicios'))

    for _, row in servicios.loc[servicios['tecnico_id'].isna() | (servicios['tecnico_id'].astype('string').str.strip() == ''), ['servicio_id']].iterrows():
        issues.append(_issue('R002', 'ALTA', 'servicio', str(row['servicio_id']), 'servicio_sin_tecnico', 'El servicio no posee tecnico_id asociado.', 'servicios'))

    estados = servicios['estado_servicio'].astype('string').str.upper().fillna('')
    for _, row in servicios.loc[~estados.isin(VALID_SERVICE_STATUSES), ['servicio_id', 'estado_servicio']].iterrows():
        issues.append(_issue('R003', 'MEDIA', 'servicio', str(row['servicio_id']), 'estado_invalido', f"Estado no contemplado: {row['estado_servicio']}", 'servicios'))

    for _, row in servicios.loc[servicios['horario'].isna() | (servicios['horario'].astype('string').str.strip() == ''), ['servicio_id']].iterrows():
        issues.append(_issue('R004', 'MEDIA', 'servicio', str(row['servicio_id']), 'horario_faltante', 'El servicio no posee horario informado.', 'servicios'))

    for _, row in servicios.loc[servicios['servicios'].astype('string').fillna('').str.contains(','), ['servicio_id', 'servicios']].iterrows():
        issues.append(_issue('R005', 'BAJA', 'servicio', str(row['servicio_id']), 'servicio_multi_tipo', f"Campo compuesto: {row['servicios']}", 'servicios'))

    dup_mask = servicios.duplicated(subset=['cliente_id', 'tecnico_id', 'horario', 'estado_servicio'], keep=False)
    for _, row in servicios.loc[dup_mask, ['servicio_id']].iterrows():
        issues.append(_issue('R006', 'MEDIA', 'servicio', str(row['servicio_id']), 'duplicado_potencial', 'Posible duplicado por combinacion de campos clave.', 'servicios'))

    merged = servicios[['servicio_id', 'tecnico_id']].merge(tecnicos, on='tecnico_id', how='left')
    for _, row in merged.loc[merged['activo'] == False, ['servicio_id', 'tecnico_id']].iterrows():
        issues.append(_issue('R007', 'MEDIA', 'servicio', str(row['servicio_id']), 'tecnico_inactivo_referenciado', f"Servicio referencia tecnico inactivo: {row['tecnico_id']}", 'servicios'))

    cols = ['rule_id', 'severity', 'entity_type', 'entity_id', 'issue_type', 'issue_description', 'source_table']
    return pd.DataFrame(issues, columns=cols)


def summarize_issues(issues_df: pd.DataFrame) -> pd.DataFrame:
    if issues_df.empty:
        return pd.DataFrame(columns=['issue_type', 'severity', 'cantidad'])
    return (
        issues_df.groupby(['issue_type', 'severity'], as_index=False)
        .size()
        .rename(columns={'size': 'cantidad'})
        .sort_values(by=['cantidad', 'issue_type'], ascending=[False, True])
        .reset_index(drop=True)
    )

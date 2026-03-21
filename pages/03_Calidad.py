from src.ingest.loaders import run_initial_load
from src.quality.rules import evaluate_quality_rules, summarize_issues
import streamlit as st


def load_quality_data():
    dataframes = run_initial_load()
    issues_df = evaluate_quality_rules(dataframes)
    summary_df = summarize_issues(issues_df)
    return issues_df, summary_df


def main():
    st.title('Calidad de datos')
    st.write('Hallazgos e inconsistencias detectadas sobre las fuentes integradas del prototipo.')

    try:
        issues_df, summary_df = load_quality_data()
    except Exception as exc:
        st.error(str(exc))
        return

    st.subheader('Resumen general')
    st.write('Total de hallazgos:', len(issues_df))

    if not summary_df.empty:
        severidades = sorted(summary_df['severity'].dropna().astype(str).unique().tolist())
        st.write('Severidades detectadas:', ', '.join(severidades))
    else:
        st.write('Severidades detectadas: ninguna')

    st.subheader('Resumen por tipo y severidad')
    if summary_df.empty:
        st.write('No se detectaron inconsistencias con las reglas actuales.')
    else:
        st.dataframe(summary_df)

    st.subheader('Detalle de hallazgos')
    if issues_df.empty:
        st.write('Sin hallazgos para mostrar.')
    else:
        severity_options = ['Todas'] + sorted(issues_df['severity'].dropna().astype(str).unique().tolist())
        issue_options = ['Todos'] + sorted(issues_df['issue_type'].dropna().astype(str).unique().tolist())

        selected_severity = st.selectbox('Filtrar por severidad', severity_options)
        selected_issue = st.selectbox('Filtrar por tipo de hallazgo', issue_options)

        filtered = issues_df.copy()
        if selected_severity != 'Todas':
            filtered = filtered[filtered['severity'] == selected_severity]
        if selected_issue != 'Todos':
            filtered = filtered[filtered['issue_type'] == selected_issue]

        st.write('Hallazgos filtrados:', len(filtered))
        st.dataframe(filtered)

    st.write('Esta página permite mostrar cómo el prototipo detecta problemas de estructura y calidad en los datos fuente.')


if __name__ == '__main__':
    main()

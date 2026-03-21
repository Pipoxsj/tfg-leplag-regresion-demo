from src.ingest.loaders import run_initial_load
from src.quality.rules import evaluate_quality_rules, summarize_issues


def main():
    print("=" * 70)
    print("QUALITY CHECK - PROTOTIPO LEPLAG")
    print("=" * 70)

    dataframes = run_initial_load()
    issues_df = evaluate_quality_rules(dataframes)
    summary_df = summarize_issues(issues_df)

    print("\n=== RESUMEN DE HALLAZGOS ===")
    if summary_df.empty:
        print("No se detectaron inconsistencias con las reglas actuales.")
    else:
        print(summary_df)

    print("\n=== DETALLE DE HALLAZGOS ===")
    if issues_df.empty:
        print("Sin hallazgos para mostrar.")
    else:
        print(issues_df)

    print("\n" + "=" * 70)
    print(f"TOTAL DE HALLAZGOS: {len(issues_df)}")
    print("=" * 70)


if __name__ == "__main__":
    main()

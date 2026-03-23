from backend.agents.query_agent import generate_sql
from backend.db.snowflake_connector import run_query
from backend.agents.profiling_agent import (
    null_check,
    duplicate_summary,
    schema_validation,
    timeliness_check,
    consistency_check,
    accuracy_check,
    completeness_score
)
from backend.agents.report_agent import generate_html_report


def run_full_pipeline(question: str, table: str):
    sql = generate_sql(question)
    data = run_query(sql)

    quality_results = {
        "nulls": null_check(table),
        "duplicates": duplicate_summary(table),
        "schema": schema_validation(table),
        "timeliness": timeliness_check(table),
        "consistency": consistency_check(table),
        "accuracy": accuracy_check(table),
        "completeness": completeness_score(table),
    }

    html_report = generate_html_report(quality_results)
    
    return html_report
# API routes for agents
#from fastapi import APIRouter
#from backend.agents.query_agent import generate_sql

#router = APIRouter()

#@router.post("/nl-to-sql")
#def nl_to_sql(question: str):

 #   sql = generate_sql(question)

 #   return {"sql_query": sql}
from fastapi import APIRouter
from backend.agents.query_agent import generate_sql
from backend.db.snowflake_connector import run_query
# ===== Imports =====
from fastapi import FastAPI


# ===== App Instance =====
app = FastAPI()



router = APIRouter()

@router.get("/generate-sql")
def generate_sql_endpoint(question: str):
    sql = generate_sql(question)
    result = run_query(sql)

    return {
        "generated_sql": sql,
        "result": result
    }


from backend.agents.profiling_agent import null_check, duplicate_summary, schema_validation,accuracy_check,completeness_score, consistency_check,status_consistency_check, rating_consistency_check, numeric_consistency_check


@router.get("/null-check")
def null_check_endpoint():
    return null_check("NAND_DB.PUBLIC.UBER_RIDE_DETAILS")

@router.get("/duplicate-check")
def duplicate_check_endpoint():
    return duplicate_summary("NAND_DB.PUBLIC.UBER_RIDE_DETAILS")

@router.get("/schema-check")
def schema_check_endpoint():
    return schema_validation("NAND_DB.PUBLIC.UBER_RIDE_DETAILS")

@router.get("/accuracy-check")
def accuracy_endpoint(table: str):
    return accuracy_check(table)

@router.get("/completeness-check")
def completeness_endpoint(table: str):
    return completeness_score(table)

@router.get("/consistency-check")
def consistency_endpoint(table: str):
    return consistency_check(table)

from fastapi.responses import HTMLResponse
from backend.agents.report_agent import generate_html_report

@router.get("/generate-report", response_class=HTMLResponse)
def report_endpoint(table: str):
    results = {
        "nulls": null_check(table),
        "duplicates": duplicate_summary(table),
        "completeness": completeness_score(table),
        "accuracy": accuracy_check(table)
    }

    html = generate_html_report(results)
    return html

# from backend.agents.orchestrator import run_full_pipeline


# @router.get("/run-analysis")
# def run_analysis(question: str, table: str):
#     return run_full_pipeline(question, table)

# from fastapi.responses import HTMLResponse

# @router.get("/run-analysis", response_class=HTMLResponse)
# def run_analysis(...):
#     ...
#     return html_report

from fastapi.responses import HTMLResponse
from backend.agents.orchestrator import run_full_pipeline

@router.get("/run-analysis", response_class=HTMLResponse)
def run_analysis(question: str, table: str):
    html_report = run_full_pipeline(question, table)
    return html_report
app.include_router(router)
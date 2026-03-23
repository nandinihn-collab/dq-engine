# FastAPI main entry
from fastapi import FastAPI
from backend.api.routes import router
from backend.agents.profiling_agent import (
    status_consistency_check,
    rating_consistency_check,
    numeric_consistency_check
)

app = FastAPI()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Data Quality Engine Running"}


@app.get("/timeliness-check")
def timeliness(table: str, column: str):
    from backend.agents.profiling_agent import timeliness_check
    return timeliness_check(table, column)


@app.get("/consistency-status")
def consistency_status(table: str):
    return status_consistency_check(table)

@app.get("/consistency-ratings")
def consistency_ratings(table: str):
    return rating_consistency_check(table)

@app.get("/consistency-numeric")
def consistency_numeric(table: str):
    return numeric_consistency_check(table)

@app.get("/timeliness-check")
def timeliness(table: str):
    return timeliness_check(table)


@app.get("/accuracy-check")
def accuracy(table: str):
    return accuracy_check(table)


@app.get("/completeness-score")
def completeness(table: str):
    return completeness_score(table)





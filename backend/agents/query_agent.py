from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

# 🔥 Load .env file
load_dotenv()

prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a SQL expert.

Use Snowflake SQL.

Table:
NAND_DB.PUBLIC.UBER_RIDE_DETAILS

Columns:
- DATE
- TIME
- BOOKING_ID
- BOOKING_STATUS
- CUSTOMER_ID
- VEHICLE_TYPE
- PICKUP_LOCATION
- DROP_LOCATION
- AVG_VTAT
- AVG_CTAT
- CANCELLED_RIDES_BY_CUSTOMER

Rules:
- Only return SQL query
- No explanation

Question:
{question}

SQL Query:
"""
)

# ✅ Now this will work
llm = OpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def generate_sql(question: str):
    formatted_prompt = prompt.format(question=question)
    response = llm.invoke(formatted_prompt)
    return str(response)
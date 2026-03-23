from agents.query_agent import generate_sql

question = "Show all customers with missing email"

sql = generate_sql(question)

print(sql)

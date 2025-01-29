from langchain_community.agent_toolkits.sql.base import create_sql_agent
from connection import llm, db

# ✅ Override Agent SQL Execution
def execute_sql(query):
    print("\n🔍 Debugging LangChain Agent Query Execution")
    print(f"Raw Query from LangChain:\n{query}")

    try:
        compiled_query = text(query)  # ✅ Force text() wrapping
        print("✅ Query After text() Wrapping:\n", compiled_query)

        with db._engine.connect() as conn:
            result = conn.execute(compiled_query)
            rows = result.fetchall()

            print("✅ Query Success - Rows:", len(rows))
            return rows
    except Exception as e:
        print("❌ Query Execution Error:", str(e))
        return f"Query Execution Error: {e}"

# ✅ Ensure LangChain Agent Uses the Custom Database Wrapper
sql_agent = create_sql_agent(
    llm=llm,  # OpenAI or other LLM
    db=db,  # SQLAlchemy connection to Dremio
    verbose=True,  # Enable verbose logging
    handle_parsing_errors=True  # ✅ Handle parsing issues more gracefully
)

# ✅ Force Agent to Use Correct Execution
sql_agent.query_executor = execute_sql

print('before test')
sql_agent.query_executor('SELECT TABLE_NAME FROM INFORMATION_SCHEMA."TABLES"')
print('after test')
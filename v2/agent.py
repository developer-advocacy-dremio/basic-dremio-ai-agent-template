from langchain_community.agent_toolkits.sql.base import create_sql_agent
from connection import llm, db

# ✅ Create SQL Agent with the Custom Database Wrapper
sql_agent = create_sql_agent(
    llm=llm,  # OpenAI LLM
    db=db,  # ✅ Custom DremioSQLDatabase with fixed execution
    verbose=True,
    handle_parsing_errors=True  # ✅ Handle parsing issues more gracefully
)

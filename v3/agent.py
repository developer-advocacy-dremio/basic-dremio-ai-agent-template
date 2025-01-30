from langchain_community.agent_toolkits.sql.base import create_sql_agent
from connection import dremio
from DremioSQLDatabase import DremioSQLDatabase
from langchain_community.llms import OpenAI

# ✅ Initialize the Custom Database for LangChain
db = DremioSQLDatabase(dremio)

# ✅ Initialize OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

# ✅ Create SQL Agent with the Custom Database Wrapper
sql_agent = create_sql_agent(
    llm=llm,  # OpenAI LLM
    db=db,  # ✅ Custom DremioSQLDatabase with optimized execution
    verbose=True,
    handle_parsing_errors=True  # ✅ Handle parsing issues more gracefully
)

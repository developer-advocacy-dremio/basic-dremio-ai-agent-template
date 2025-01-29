from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
from langchain_community.llms import OpenAI
from env import DREMIO_ODBC_URI

# ✅ Create SQLAlchemy engine
engine = create_engine(DREMIO_ODBC_URI)

# ✅ Custom Wrapper to Ensure Queries Use text()
class DremioSQLDatabase(SQLDatabase):
    def run(self, query: str):
        """Ensures queries are wrapped in text() before execution."""
        print("\n🔍 SQLDatabase Received Query:", query)

        try:
            compiled_query = text(query)  # ✅ Ensure text() wrapping
            print("✅ Query Wrapped with text():", compiled_query)

            with self._engine.connect() as conn:
                result = conn.execute(compiled_query)
                rows = result.fetchall()

                print("✅ Query Execution Success - Rows:", len(rows))
                return rows
        except Exception as e:
            print("❌ SQL Execution Error:", e)
            return f"SQL Execution Error: {e}"

# ✅ Get the list of available user tables (without INFORMATION_SCHEMA)
with engine.connect() as conn:
    result = conn.execute(text('SELECT TABLE_NAME FROM INFORMATION_SCHEMA."TABLES"'))
    user_tables = [row[0] for row in result.fetchall() if not row[0].startswith("INFORMATION_SCHEMA")]

print("Using Tables:", user_tables)

# ✅ Use the custom SQLDatabase wrapper
db = DremioSQLDatabase(engine, include_tables=user_tables)

# ✅ Initialize OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)

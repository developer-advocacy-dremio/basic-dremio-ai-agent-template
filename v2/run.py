import sys
from agent import sql_agent

# Define a natural language question
question = sys.argv[1] if len(sys.argv) > 1 else "What is the average temperature in NYC?"

prompt = f"""
You are an expert SQL agent working with a Dremio database to answer the follow question "{question}".
Before generating a query, check for the tables fully qualified name and check the schema of the relevant table(s) .Use `INFORMATION_SCHEMA.COLUMNS` to verify available columns before writing the final query.

### Example Thought Process:
1️⃣ **First, fetch the column names**:
SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '<table_name>'

2️⃣ **Then, only use valid column names** when constructing the final SQL query.

Follow these steps every time you generate a SQL query. Ensure your queries are well-formatted and valid.
"""

print("\n🚀 Running Query Through Agent...")
response = sql_agent.run(question)

print("\n✅ Agent Response:\n", response)


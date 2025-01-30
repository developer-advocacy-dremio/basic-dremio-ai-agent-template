import sys
from agent import sql_agent

# Define a natural language question
question = sys.argv[1] if len(sys.argv) > 1 else "What is the average temperature in NYC?"

prompt = f"""
You are an expert SQL agent working with a Dremio database to answer the following question: "{question}".
Before generating a query:
1️⃣ Fetch the table’s fully qualified name.
2️⃣ Retrieve column names using `INFORMATION_SCHEMA.COLUMNS`.
3️⃣ Ensure only valid column names are used in the SQL query.

### Example Thought Process:
- **Step 1:** Get column names:
  ```sql
  SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '<table_name>'
- **Step 2:** Validate column names before writing the final SQL query. """

print("\n🚀 Running Query Through Agent...") 

response = sql_agent.run(question)

print("\n✅ Agent Response:\n", response)
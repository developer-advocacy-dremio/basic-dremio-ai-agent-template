import sys
from agent import sql_agent

# Define a natural language question
question = sys.argv[1] if len(sys.argv) > 1 else "What is the average temperature in NYC?"

# Let the agent generate and execute SQL against Dremio
response = sql_agent.run(question)

# Print the result
print(response)

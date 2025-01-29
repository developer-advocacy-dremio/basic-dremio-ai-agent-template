# SQL Query Execution Script Documentation

## Overview
The `run.py` module serves as the entry point for executing natural language queries against a Dremio database. It leverages the SQL agent, which translates user input into SQL queries and retrieves results dynamically.

## Dependencies
This script imports:
- `sys` for command-line argument handling.
- `sql_agent` from `agent.py`, which is responsible for translating and executing natural language queries as SQL.

## Execution Flow
1. **User Input Handling**  
   - The script takes a user-provided query as a command-line argument.  
   - If no argument is provided, it defaults to the question: *"What is the average temperature in NYC?"*  

2. **Query Preprocessing & Validation**  
   - A system prompt is created to guide the SQL agent in structuring its approach.  
   - The prompt ensures that:
     - Fully qualified table names are verified.
     - Table schemas are checked via `INFORMATION_SCHEMA.COLUMNS` before query generation.
     - Only valid column names are included in the final SQL statement.  
   - The prompt follows a structured thought process:
     1. **Retrieve column names** using `INFORMATION_SCHEMA.COLUMNS`.
     2. **Construct a query** with only verified column names.

3. **Executing the Query with the SQL Agent**  
   - The script prints a message indicating the query execution has started.  
   - The `sql_agent.run(question)` method processes the natural language question, converting it into a valid SQL query and executing it against the Dremio database.

4. **Displaying Results**  
   - The script prints the agent's response, displaying the query result retrieved from the database.

## Summary
- Accepts a natural language question as input.
- Guides the SQL agent to verify table schemas before query generation.
- Converts the user query into a well-formatted SQL statement.
- Executes the query against Dremio and prints the results.
- Ensures accuracy by validating table and column names before execution.

This script enables users to interact with Dremio using natural language queries while ensuring robust SQL query generation and execution.

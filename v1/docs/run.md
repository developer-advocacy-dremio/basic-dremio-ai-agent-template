# Script: Agent Query Executor

## Description
This script integrates a LangChain agent to process natural language questions, run a corresponding SQL query on a dataset, and return the results. It combines a user-provided question with a predefined SQL query, executes the query via the agent, and outputs the response.

---

## Requirements

### **Dependencies**
- `LangChain` and a compatible agent setup.
- A custom `truncate` module (optional, for truncating input to ensure token limits).
- The `initialize_agent` module, which contains the pre-configured LangChain agent.
- Python 3.6 or later.


## Script Overview

#### Inputs

- The script accepts a natural language question as a command-line argument.
- If no argument is provided, it defaults to `"What is the average temperature in NYC?"`.

#### Query
A predefined SQL query fetches data for answering the question.

#### Agent
Combines the user question and SQL query into a single input for the agent to process.
The agent executes the query and generates a response.

#### Code Breakdown

1. Importing Dependencies
```python
import sys
from initialize_agent import agent
from truncate import truncate_string
```
- sys: For capturing command-line arguments.
- initialize_agent: Provides the pre-configured LangChain agent.
- truncate_string: Optional utility to truncate long inputs (not actively used here).

2. Main Logic

```python
if __name__ == "__main__":
    # Example question for the agent
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the average temperature in NYC?"

    # SQL query to fetch the required data
    query = """
    SELECT station, "name", "date", awnd, prcp, snow, snwd, tempmax, tempmin  
    FROM Samples."samples.dremio.com"."NYC-weather.csv" LIMIT 3000;
    """

    # Combine the question and query for the agent
    response = agent.run(f"Answer the question: {question} with this Data: {query}")
    print(response)
```

### Explanation
Input Handling:

- The script checks for a command-line argument:
    - If provided, it uses the argument as the question.
    - If not, it defaults to "What is the average temperature in NYC?".

SQL Query:

- A predefined SQL query retrieves weather data, including fields such as station, name, date, tempmax, and tempmin.
Limits the results to 3,000 rows.

Agent Execution:

- Combines the natural language question and SQL query into a single input string for the agent.
- Calls the agent's run method to execute the query and generate a response.

Output:

Prints the agent's response to the console.

## Usage

**Command-Line Execution**
Run the script using the command line. Provide a question as an argument or allow it to use the default question:

```bash
python script.py "What is the maximum snowfall recorded in NYC?"
```
Example Output:

```csharp
Answering your question: The maximum snowfall recorded in NYC is 12.5 inches on January 23, 2016.
```
Default Execution
If no question is provided:

```bash
python script.py
```

Output:

```csharp
Answering your question: The average temperature in NYC is 52°F.
```

## Notes

**Token Limits:**

If the combined input exceeds the token limit of the language model, use the `truncate_string` utility to truncate the input before sending it to the agent.

**SQL Query:**

Ensure the dataset and query are correct and valid for the Dremio instance or database used.

**Agent Configuration:**

The agent's behavior depends on the initialize_agent configuration, including connected tools, LLMs, and processing logic.

## Suggested Enhancements
**Dynamic Query Generation:**

Allow the script to dynamically generate SQL queries based on the user-provided question.

**Truncation Integration:**

Incorporate the truncate_string utility to ensure inputs stay within token limits.

**Error Handling:**

Add error handling for invalid questions, SQL errors, or agent execution issues.

**Verbose Mode:**

Add a verbose mode for logging agent decisions during execution.
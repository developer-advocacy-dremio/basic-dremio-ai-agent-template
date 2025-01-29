# LangChain Agent with DremioQueryTool

## Description

This script initializes a LangChain agent that integrates the `DremioQueryTool` for querying data from Dremio and an OpenAI language model (LLM) for natural language processing. The agent supports querying Dremio Cloud or Dremio Software, based on the environment configuration.

## Requirements

### **Dependencies**
- **LangChain**: A framework for building applications with LLMs.
- **LangChain Community LLMs**: For using OpenAI's language models.
- **DremioQueryTool**: A custom LangChain tool for querying Dremio.
- **Environment Configuration**: Ensure `DREMIO_ENVIRONMENT` is defined in your environment or `.env` file.

## Environment Variable
The following variable must be set in the env.py file or through environment variables:

- `DREMIO_ENVIRONMENT`:	Specifies the Dremio connection mode: "cloud" or "software".

## Components

1. `DremioQueryTool`
The `DremioQueryTool` is initialized using the DREMIO_ENVIRONMENT variable to determine the mode (cloud or software) for connecting to Dremio. It enables querying Dremio directly with SQL.

```python
dremio_tool = DremioQueryTool(mode=DREMIO_ENVIRONMENT)
```

2. LangChain Tool Wrapping
The DremioQueryTool is wrapped in a LangChain Tool object to integrate it with the LangChain agent.

| **Attribute**  | **Description**                                                                |
|-----------------|-------------------------------------------------------------------------------|
| `name`         | The name of the tool, inherited from `DremioQueryTool`.                       |
| `func`         | The method to execute the tool's functionality (`dremio_tool.run`).           |
| `description`  | A brief explanation of the tool's capabilities.                               |

```python
tools = [Tool(name=dremio_tool.name, func=dremio_tool.run, description=dremio_tool.description)]
```

3. OpenAI LLM

- An OpenAI language model (gpt-3.5-turbo-instruct) is initialized for generating responses based on the queries and data.

| **Parameter**   | **Value**                   | **Description**                                      |
|------------------|-----------------------------|----------------------------------------------------|
| `model`         | `"gpt-3.5-turbo-instruct"`  | Specifies the OpenAI model to use.                 |
| `temperature`   | `0`                         | Controls randomness of responses (0 = deterministic). |
                            |


```python
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)
```

4. LangChain Agent

The LangChain agent is created with the tools and the OpenAI LLM. It uses the `ZERO_SHOT_REACT_DESCRIPTION` agent type, which allows the agent to decide how to use the tool dynamically based on the user's input.

| **Parameter**   | **Description**                                                          |
|------------------|--------------------------------------------------------------------------|
| `tools`         | A list of tools the agent can use (`dremio_tool` in this case).          |
| `llm`           | The OpenAI language model used for natural language understanding.       |
| `agent`         | The agent type, here `ZERO_SHOT_REACT_DESCRIPTION`.                      |
| `verbose`       | Whether to log additional information during agent execution.            |

```python
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
```

## Usage
1. Environment Setup
Ensure DREMIO_ENVIRONMENT is correctly set in the env.py file or environment variables:

Example .env file:

```dotenv
DREMIO_ENVIRONMENT=cloud
```

2. Run the Agent
The agent can now be used to execute queries and process results. Example:

```python
# Define a query and a question
query = """
SELECT station, "name", "date", tempmax, tempmin
FROM Samples."samples.dremio.com"."NYC-weather.csv";
"""
question = "What is the highest temperature recorded in this dataset?"

# Combine query and question
response = agent.run(f"Run this query: {query} and answer the question: {question}")

# Print the result
print(response)
```

## Notes
Dremio Mode:

- `"cloud"` mode requires DREMIO_TOKEN and DREMIO_URI for authentication.
- `"software"` mode requires DREMIO_USERNAME, DREMIO_PASSWORD, DREMIO_LOGIN_URI, and DREMIO_URI.

## Error Handling:

Ensure valid SQL queries are provided to avoid errors during query execution.

**Verbose Mode:**

- Setting verbose=True logs detailed information about the agent's decision-making process.

#### Example Workflow
- Configure the environment variable for the Dremio mode (e.g., "cloud" or "software").
- Define SQL queries to fetch data from Dremio.
- Use natural language questions to interact with the agent.
- The agent queries Dremio using DremioQueryTool and processes the results via the OpenAI LLM.

## Limitations

**Asynchronous Queries:**
The agent does not support asynchronous query execution.

**OpenAI Token Limits:**
Ensure the combined input and output tokens stay within the model's token limit (e.g., 4,097 tokens for gpt-3.5-turbo).

## Suggested Enhancements
**Token Truncation:** Add functionality to truncate SQL queries and user questions to fit within token limits.

**Async Support:** Implement asynchronous support for the agent to improve scalability.

**Custom Models:** Integrate support for local LLMs using Hugging Face models for cost-efficient operations.

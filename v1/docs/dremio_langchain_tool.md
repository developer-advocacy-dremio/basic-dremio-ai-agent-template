# DremioQueryTool Documentation

## Description
The `DremioQueryTool` is a custom LangChain tool designed to query data from a Dremio instance. It supports both **Dremio Cloud** and **Dremio Software** modes and uses a `DremioConnection` object to execute SQL queries. Query results are returned as formatted strings for easy integration with LangChain workflows.


## Class: `DremioQueryTool`

### **Attributes**
| Attribute      | Type   | Default             | Description                                                                                  |
|----------------|--------|---------------------|----------------------------------------------------------------------------------------------|
| `name`         | `str`  | `"DremioQueryTool"` | The name of the tool.                                                                        |
| `description`  | `str`  | See description     | A brief explanation of the tool, including its purpose and capabilities.                     |
| `mode`         | `str`  | `"software"`        | The mode for connecting to Dremio, either `"cloud"` or `"software"`.                         |
| `connection`   | `object` | `None`            | The Dremio connection object, initialized using the `get_dremio_connection` function.        |


### **Initialization**

#### **Constructor**
```python
def __init__(self, mode: str = "software"):
```

**Description**: Initializes the DremioQueryTool and establishes a connection to Dremio based on the specified mode.

#### Parameters:
- `mode (str)`: Specifies whether to connect to Dremio Cloud ("cloud") or Dremio Software ("software"). Default is "software".

#### Behavior:
- Calls the `get_dremio_connection` function to set up the connection attribute.

- Inherits initialization behavior from BaseTool.

#### Methods
**1. _run**

```python
def _run(self, query: str) -> str:
```

`Description`: Executes the provided SQL query and returns the results as a formatted string.

_Parameters:_
- `query (str)`: The SQL query to be executed.
Returns:
- `str`: The query results formatted as a string (from a Pandas DataFrame).

_Error Handling:_
If an exception occurs during query execution, an error message is returned instead.

_Example Usage_

```python
tool = DremioQueryTool(mode="cloud")
result = tool._run("SELECT * FROM samples.table_name LIMIT 10;")
print(result)
# Output: Formatted DataFrame string of query results
```

2. **_arun**

```python
async def _arun(self, query: str) -> str:
```

- `Description`: Asynchronous version of the _run method. This method is not implemented and raises a `NotImplementedError`.

_Parameters:_
- `query (str)`: The SQL query to be executed asynchronously.

_Raises:_

- `NotImplementedError`: Indicates that async execution is not supported.

_Example Usage_

```python
try:
    await tool._arun("SELECT * FROM samples.table_name LIMIT 10;")
except NotImplementedError as e:
    print(e)
# Output: "DremioQueryTool does not support async execution yet."
```

## Usage Workflow
- **Initialize the Tool**: Create an instance of the DremioQueryTool by specifying the connection mode ("cloud" or "software").

- **Run Queries**: Use the _run method to execute SQL queries and retrieve results as a string.

_Code Example_
```python
from dremio_query_tool import DremioQueryTool

# Initialize the tool in "cloud" mode
tool = DremioQueryTool(mode="cloud")

# Define a query
query = """
SELECT station, "name", "date", awnd, prcp, snow, snwd, tempmax, tempmin
FROM Samples."samples.dremio.com"."NYC-weather.csv";
"""

# Execute the query
result = tool._run(query)

# Print the results
print(result)
```

## Notes
- **Error Handling**: The _run method gracefully handles exceptions by returning the error message. Ensure the query is valid to avoid errors.

#### Dremio Modes:
- `"cloud"`: Requires DREMIO_TOKEN and DREMIO_URI for authentication.
- `"software"`: Requires DREMIO_USERNAME, DREMIO_PASSWORD, DREMIO_LOGIN_URI, and DREMIO_URI for authentication.

**Tool Integration:** The DremioQueryTool can be integrated into a LangChain agent for enhanced query execution in workflows.
Limitations

**No Async Support:** The _arun method is not implemented, so the tool does not support asynchronous query execution.

**Output Format:** Results are returned as a formatted string, which may not be ideal for large datasets.

## Suggested Enhancements
- **Async Support:** Implement the _arun method for asynchronous query execution.
- **Custom Output Options:** Allow results to be returned in different formats, such as JSON, CSV, or raw DataFrame.
- **Token Caching:** For software mode, cache the authentication token to avoid repeated API calls.
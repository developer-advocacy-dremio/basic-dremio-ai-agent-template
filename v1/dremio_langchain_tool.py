from langchain.tools import BaseTool
from dremio_connect import get_dremio_connection

class DremioQueryTool(BaseTool):
    """
    A LangChain tool to query data from Dremio using the Dremio connection.
    """

    name: str = "DremioQueryTool"  # Type annotation for tool name
    description: str = (
        "This tool queries data from Dremio. Provide a valid SQL query to fetch results. "
        "It supports both Dremio Cloud and Dremio Software modes. Ensure the query is valid."
    )  # Type annotation for tool description
    mode: str  # Declare mode as a required field
    connection: object = None  # Declare connection as a field, defaulting to None

    def __init__(self, mode: str = "software"):
        """
        Initialize the DremioQueryTool with the appropriate Dremio connection mode.

        Args:
            mode (str): "cloud" or "software" (default is "software").
        """
        # Initialize parent class with mode
        super().__init__(mode=mode)

        # Set up Dremio connection
        self.connection = get_dremio_connection(mode=mode)

    def _run(self, query: str) -> str:
        """
        Execute the provided SQL query and return the results as a string.

        Args:
            query (str): The SQL query to execute.

        Returns:
            str: Query results as a string.
        """
        try:
            # Execute the query and fetch results as a Pandas DataFrame
            df = self.connection.toPandas(query)
            return df.to_string(index=False)  # Return the DataFrame as a formatted string
        except Exception as e:
            return f"Error executing query: {e}"

    async def _arun(self, query: str) -> str:
        """
        Asynchronous version of the run method (not implemented).
        """
        raise NotImplementedError("DremioQueryTool does not support async execution yet.")

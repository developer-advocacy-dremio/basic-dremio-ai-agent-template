import re
from typing import Union, Optional, Dict, Any, Sequence
from dremio_simple_query.connect import DremioConnection, get_token
from langchain_community.llms import OpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from os import getenv
from dotenv import load_dotenv
import pandas as pd

# ✅ Load environment variables
load_dotenv()

# 🔹 Dremio Configuration
DREMIO_ENVIRONMENT = getenv("DREMIO_ENVIRONMENT", "software").lower()
DREMIO_URI = getenv("DREMIO_URI")
DREMIO_TOKEN = getenv("DREMIO_TOKEN")
DREMIO_USERNAME = getenv("DREMIO_USERNAME")
DREMIO_PASSWORD = getenv("DREMIO_PASSWORD")
DREMIO_LOGIN_URI = getenv("DREMIO_LOGIN_URI")

# 🔹 Get Dremio Token for Software Deployments
def get_dremio_token():
    """Fetches a token from the Dremio Software API if required."""
    if DREMIO_ENVIRONMENT == "software":
        print("🔄 Fetching Dremio Software Token...")
        payload = {"userName": DREMIO_USERNAME, "password": DREMIO_PASSWORD}
        return get_token(uri=DREMIO_LOGIN_URI, payload=payload)
    return DREMIO_TOKEN  # Return predefined token for Dremio Cloud

# ✅ Establish Dremio connection
DREMIO_AUTH_TOKEN = get_dremio_token()
dremio = DremioConnection(DREMIO_AUTH_TOKEN, DREMIO_URI)

# ✅ Custom LangChain-Compatible SQL Database Wrapper
class DremioSQLDatabase(SQLDatabase):
    def __init__(self, dremio_connection: DremioConnection):
        """
        Initializes the Dremio SQLDatabase wrapper.
        """
        self.dremio_connection = dremio_connection  # ✅ Ensure connection is properly stored!

    def run(
        self,
        command: Union[str, Any],  # Can be a string query or an Executable
        fetch: str = "all",  # Options: 'all', 'one', 'cursor'
        include_columns: bool = False, 
        *,
        parameters: Optional[Dict[str, Any]] = None,  # Query parameters
        execution_options: Optional[Dict[str, Any]] = None
    ) -> Union[str, Sequence[Dict[str, Any]], Any]:
        """
        Executes a SQL query and fetches results as needed.
        """
        print("\n🔍 Received Query:", command)
        print("🔢 Parameters:", parameters)

        if isinstance(command, str):  # Ensure query is a string
            query = command
        else:
            query = str(command)  # Convert Executable object to string

        # Inject parameters into query safely
        if parameters:
            query = self._inject_parameters(query, parameters)

        print("✅ Final Query Sent to Dremio:", query)

        try:
            df: DataFrame = self.dremio_connection.toPandas(query)  # ✅ Run query with stored connection
            print("✅ Query Successful! Rows Returned:", len(df))

            if fetch == "one":
                return df.iloc[0].to_dict() if not df.empty else {}
            elif fetch == "cursor":
                return df  # Return DataFrame as an alternative cursor-like object
            else:
                return df.to_dict(orient="records")  # Default: return all rows
        except Exception as e:
            print("❌ Query Execution Failed:", str(e))
            return f"Query Execution Error: {e}"

    def run_no_throw(
        self,
        command: str,
        fetch: str = "all",
        include_columns: bool = False,
        *,
        parameters: Optional[Dict[str, Any]] = None,
        execution_options: Optional[Dict[str, Any]] = None
    ) -> Union[str, Sequence[Dict[str, Any]]]:
        """
        Executes SQL query but does not throw exceptions on failure.
        """
        try:
            return self.run(command, fetch, include_columns, parameters=parameters, execution_options=execution_options)
        except Exception as e:
            return f"Query Execution Error: {e}"

    def _inject_parameters(self, query: str, parameters: Dict[str, Any]) -> str:
        """
        Safely injects parameters into the query string.
        """
        for key, value in parameters.items():
            sanitized_value = self._sanitize_value(value)
            query = query.replace(f":{key}", sanitized_value)  # Replace placeholders
        return query

    def _sanitize_value(self, value):
        """Ensures safe and correctly formatted SQL values."""
        if isinstance(value, str):
            return "'{}'".format(value.replace("'", "''"))  # Properly escape single quotes
        elif isinstance(value, (int, float)):
            return str(value)  # Use raw numeric values
        else:
            return "NULL"  # Default fallback

    def get_usable_table_names(self):
        """Returns a list of available table names."""
        try:
            query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA."TABLES"'
            df = self.dremio_connection.toPandas(query)
            table_names = df.iloc[:, 0].tolist()  # Extract first column as list
            print("📋 Available Tables:", table_names)
            return table_names
        except Exception as e:
            print("❌ Error Fetching Tables:", e)
            return []

    @property
    def dialect(self):
        """Mock dialect to satisfy LangChain's SQLDatabase expectations."""
        return "dremio"

    def get_inspector(self):
        """Returns a mock inspector to prevent LangChain errors."""
        class MockInspector:
            def get_schema_names(self):
                return []
        return MockInspector()

    def get_table_info(self, table_name):
        """Returns mock table info for LangChain compatibility."""
        return {"table_name": table_name, "columns": ["dummy_col"]}

# ✅ Initialize the Custom Database for LangChain
db = DremioSQLDatabase(dremio)

# ✅ Initialize OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)




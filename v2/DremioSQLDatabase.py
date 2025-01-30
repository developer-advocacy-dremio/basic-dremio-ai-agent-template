import re
from typing import Union, Optional, Dict, Any, Sequence, List
from sqlalchemy.engine.default import DefaultDialect
from dremio_simple_query.connect import DremioConnection
from langchain_community.utilities.sql_database import SQLDatabase
import pandas as pd


class DremioSQLDatabase(SQLDatabase):
    def __init__(self, dremio_connection: DremioConnection, include_tables: Optional[List[str]] = None, exclude_tables: Optional[List[str]] = None):
        """
        Initializes the Dremio SQLDatabase wrapper, preloads schema, and ensures compatibility with LangChain.
        
        Args:
            dremio_connection (DremioConnection): Connection to Dremio.
            include_tables (Optional[List[str]]): List of specific tables to include.
            exclude_tables (Optional[List[str]]): List of tables to exclude.
        """
        self.dremio_connection = dremio_connection
        self._mock_dialect = DefaultDialect()  # ✅ Fix: Use SQLAlchemy's DefaultDialect for compatibility

        # ✅ Properties for LangChain compatibility
        self._include_tables = include_tables
        self._exclude_tables = exclude_tables

        # ✅ Dictionary to store table metadata (fully qualified names + columns)
        self._schema_info = self._load_schema_information()

    def _load_schema_information(self) -> Dict[str, Dict[str, Any]]:
        """
        Queries Dremio's INFORMATION_SCHEMA to get all tables, their fully qualified names, and their columns.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary where each table maps to its fully qualified name and column list.
        """
        schema_info = {}

        try:
            query = """
                SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                ORDER BY TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
            """
            df = self.dremio_connection.toPandas(query)

            if df.empty:
                print("⚠️ No schema information found in INFORMATION_SCHEMA.")
                return {}

            for _, row in df.iterrows():
                schema, table, column = row["TABLE_SCHEMA"], row["TABLE_NAME"], row["COLUMN_NAME"]
                fully_qualified_name = f'"{schema}"."{table}"'

                if table not in schema_info:
                    schema_info[table] = {"fully_qualified_name": fully_qualified_name, "columns": []}

                schema_info[table]["columns"].append(column)

            print(f"✅ Loaded schema for {len(schema_info)} tables from Dremio.")

        except Exception as e:
            print(f"❌ Error loading schema information: {e}")

        return schema_info

    def run(
        self,
        command: Union[str, Any], 
        fetch: str = "all",
        include_columns: bool = False, 
        *,
        parameters: Optional[Dict[str, Any]] = None,
        execution_options: Optional[Dict[str, Any]] = None
    ) -> Union[str, Sequence[Dict[str, Any]], Any]:
        """
        Executes a SQL query, ensuring:
        - Fully qualified table names
        - Sanitized column names
        - Safe parameter injection
        """
        print("\n🔍 Received Query:", command)
        print("🔢 Parameters:", parameters)

        if isinstance(command, str):
            query = command
        else:
            query = str(command)

        # 🔹 Step 1: Replace Table Names with Fully Qualified Names
        query = self._replace_table_names_with_fully_qualified(query)

        # 🔹 Step 2: Sanitize Column Names
        query = self._sanitize_query_columns(query)

        # 🔹 Step 3: Inject Parameters Safely
        if parameters:
            query = self._inject_parameters(query, parameters)

        print("✅ Final Query Sent to Dremio:", query)

        try:
            df: pd.DataFrame = self.dremio_connection.toPandas(query)
            print("✅ Query Successful! Rows Returned:", len(df))

            if fetch == "one":
                return df.iloc[0].to_dict() if not df.empty else {}
            elif fetch == "cursor":
                return df  
            else:
                return df.to_dict(orient="records")
        except Exception as e:
            print("❌ Query Execution Failed:", str(e))
            return f"Query Execution Error: {e}"

    def _replace_table_names_with_fully_qualified(self, query: str) -> str:
        """
        Identifies table names in the query and replaces them with their fully qualified versions.
        Ensures correct formatting for Dremio.
        """
        words = query.split()

        for i, word in enumerate(words):
            clean_table_name = word.strip("\"'")  # Remove potential quotes
            
            if clean_table_name in self._schema_info:
                fq_table = self._schema_info[clean_table_name]["fully_qualified_name"]
                
                # ✅ Remove unnecessary "DREMIO." prefix if present
                fq_table = fq_table.replace("DREMIO.", "")

                # ✅ Ensure correct formatting
                if fq_table.startswith('"') and fq_table.endswith('"'):
                    fq_table = fq_table  # Already properly quoted
                else:
                    fq_table = f'"{fq_table}"'  # Enclose in double quotes
                
                words[i] = fq_table  # Replace table name with correct fully qualified version

        return " ".join(words)

    def _sanitize_query_columns(self, query: str) -> str:
        """
        Ensures that column names that are Dremio keywords are properly quoted.
        """
        dremio_keywords = {"date", "timestamp", "user", "group", "order", "offset", "join"}

        words = query.split()
        for i, word in enumerate(words):
            clean_word = word.strip("\"'")  
            if clean_word.lower() in dremio_keywords and not word.startswith('"'):
                words[i] = f'"{clean_word}"' 

        return " ".join(words)

    def _inject_parameters(self, query: str, parameters: Dict[str, Any]) -> str:
        """
        Safely injects parameters into the query string.
        """
        for key, value in parameters.items():
            sanitized_value = self._sanitize_value(value)
            query = query.replace(f":{key}", sanitized_value)
        return query

    def _sanitize_value(self, value):
        """Ensures safe and correctly formatted SQL values."""
        if isinstance(value, str):
            return "'{}'".format(value.replace("'", "''"))  
        elif isinstance(value, (int, float)):
            return str(value)  
        else:
            return "NULL"  

    def get_usable_table_names(self) -> List[str]:
        """Returns a list of available table names."""
        if self._include_tables:
            return [t for t in self._schema_info if t in self._include_tables]
        elif self._exclude_tables:
            return [t for t in self._schema_info if t not in self._exclude_tables]
        return list(self._schema_info.keys())

    def get_table_info(self, table_names: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Retrieves column information and fully qualified table names for one or multiple tables.

        Args:
            table_names (Union[str, List[str]]): A table name or a list of table names.

        Returns:
            Dict[str, Any]: Dictionary containing the fully qualified name and columns.
        """
        if isinstance(table_names, list):  # ✅ Handle list input
            return {
                table: self._schema_info.get(table, {"fully_qualified_name": table, "columns": ["UNKNOWN_COLUMN"]})
                for table in table_names
            }
        
        return self._schema_info.get(table_names, {"fully_qualified_name": table_names, "columns": ["UNKNOWN_COLUMN"]})


    @property
    def dialect(self):
        """Mock dialect for LangChain compatibility."""
        return self._mock_dialect

    def get_inspector(self):
        """Returns a mock inspector to prevent LangChain errors."""
        class MockInspector:
            def get_schema_names(self):
                return []
        return MockInspector()

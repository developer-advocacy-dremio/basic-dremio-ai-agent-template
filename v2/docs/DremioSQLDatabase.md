# DremioSQLDatabase Documentation

## Overview
The `DremioSQLDatabase` class is a wrapper around Dremio that provides SQL query execution with features such as schema introspection, fully qualified table names, and compatibility with LangChain. It integrates with Dremio using the `dremio_simple_query` library and extends `SQLDatabase` from `langchain_community.utilities.sql_database`.

## Initialization
The class requires an instance of `DremioConnection` to establish a connection with the Dremio database. It optionally accepts lists of tables to include or exclude when managing schema information. During initialization, it fetches metadata from `INFORMATION_SCHEMA` to store table names, fully qualified names, and column details.

## Schema Loading
The `_load_schema_information` method retrieves metadata about tables from `INFORMATION_SCHEMA.COLUMNS`. This information is structured into a dictionary where each table name is mapped to its fully qualified name and a list of columns. The schema metadata is stored in `_schema_info`, enabling quick lookup when constructing queries.

## Query Execution
The `run` method executes SQL queries while ensuring:
- Table names are replaced with their fully qualified versions.
- Column names that are SQL keywords are properly quoted.
- Parameters are safely injected into the query.

It returns query results as dictionaries or Pandas DataFrames, depending on the requested fetch type.

## Table Name Replacement
The `_replace_table_names_with_fully_qualified` method ensures that table names in queries are replaced with their fully qualified versions stored in `_schema_info`. It avoids adding redundant prefixes like `DREMIO.` and ensures proper quoting.

## Column Name Sanitization
The `_sanitize_query_columns` method ensures that column names conflicting with Dremio SQL keywords are enclosed in double quotes. This prevents syntax errors when executing queries.

## Parameter Injection
The `_inject_parameters` method safely injects query parameters by ensuring proper escaping of string values and converting numerical values to their appropriate representations.

## Table Metadata Retrieval
The `get_usable_table_names` method returns a list of available tables, considering inclusion and exclusion lists. The `get_table_info` method retrieves column details and fully qualified names for given tables.

## Compatibility with LangChain
To maintain compatibility with LangChain, the class includes:
- A `dialect` property that returns a mock SQLAlchemy dialect.
- A `get_inspector` method that provides a mock schema inspector.

These features allow integration with LangChain agents that expect SQLAlchemy-compatible databases.

## Error Handling
The class includes exception handling when querying schema metadata or executing SQL queries. Errors are logged, and query execution failures return detailed messages to assist debugging.

## Summary
The `DremioSQLDatabase` class provides a structured way to interact with Dremio through SQL queries. It simplifies query execution by managing table metadata, ensuring proper formatting, and maintaining compatibility with LangChain.

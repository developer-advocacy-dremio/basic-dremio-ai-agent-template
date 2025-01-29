from sqlalchemy import create_engine, text
from os import environ
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DREMIO_ODBC_URI = environ.get('DREMIO_ODBC_URI')
print(DREMIO_ODBC_URI)
engine = create_engine(DREMIO_ODBC_URI)

# Test connection
with engine.connect() as conn:
    result = conn.execute(text('SELECT TABLE_NAME FROM INFORMATION_SCHEMA."TABLES"'))
    print(result.fetchall())  # Should return [(1,)]
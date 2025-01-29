import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Assign each environment variable to its own variable
DREMIO_ODBC_URI = os.getenv("DREMIO_ODBC_URI")
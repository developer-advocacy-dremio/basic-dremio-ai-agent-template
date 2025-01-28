import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Assign each environment variable to its own variable
DREMIO_TOKEN = os.getenv("DREMIO_TOKEN")
DREMIO_USERNAME = os.getenv("DREMIO_USERNAME")
DREMIO_PASSWORD = os.getenv("DREMIO_PASSWORD")
DREMIO_URI = os.getenv("DREMIO_URI")
DREMIO_LOGIN_URI = os.getenv("DREMIO_LOGIN_URI")
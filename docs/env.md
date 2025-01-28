# Environment Variable Loader

## Description
This script loads and assigns environment variables from a `.env` file to Python variables for easy access within the application. It uses the `dotenv` library to load variables and the `os` module to retrieve them. This approach ensures sensitive credentials and configuration values are managed securely and separated from the codebase.

## Environment Variables
The script expects the following environment variables to be defined in a .env file located in the root of your project:

- `DREMIO_TOKEN`: The authentication token for connecting to Dremio. (for Dremio Cloud)
- `DREMIO_USERNAME`: The username for Dremio authentication. (for Dremio Software)
- `DREMIO_PASSWORD`: The password for Dremio authentication. (for Dremio Software)
- `DREMIO_URI`: The URI of the Dremio instance. (this is the arrow flight server endpoint)
- `DREMIO_LOGIN_URI`: The login URI for obtaining an authentication token (used in Dremio software mode). (used in Dremio software )
- `DREMIO_ENVIRONMENT`: The environment mode (cloud or software) used to configure the Dremio connection.

## Script

```python
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
DREMIO_ENVIRONMENT = os.getenv("DREMIO_ENVIRONMENT")
Explanation
load_dotenv():
```

- Reads the .env file located in the current directory.
- Populates the process environment with the variables defined in the file.
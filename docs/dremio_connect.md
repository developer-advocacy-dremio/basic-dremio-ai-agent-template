# Dremio Connection Helper

## Description
This script provides a utility function, `get_dremio_connection`, to establish a connection to a Dremio instance. The connection can be configured for **Dremio Cloud** or **Dremio Software** environments based on the provided mode.

The function uses the `dremio_simple_query` library to create a `DremioConnection` object and ensures all required credentials are retrieved from environment variables.

## Dependencies
- **`dremio_simple_query`**: A library for connecting to Dremio using Arrow Flight.
- **`env`**: A file that defines the required environment variables:
  - `DREMIO_TOKEN`
  - `DREMIO_USERNAME`
  - `DREMIO_PASSWORD`
  - `DREMIO_URI`
  - `DREMIO_LOGIN_URI`

## Function: `get_dremio_connection`

### **Signature**
```python
def get_dremio_connection(mode="software") -> DremioConnection:
```

## Description
Establishes and returns a DremioConnection object. The function supports two modes:

- `cloud`: Connects to Dremio Cloud using a predefined token.
- `software`: Connects to Dremio Software by fetching an authentication token using a username and password.

## Parameters

`mode`
    - Type: `str`
    - Default: `"software"`
    - Description: Determines whether to connect to Dremio Cloud or Dremio Software.
        - `"cloud"`: Connects to Dremio Cloud using the `DREMIO_TOKEN`.
        - `"software"`: Connects to Dremio Software by fetching a token using the `DREMIO_USERNAME` and `DREMIO_PASSWORD`.

## Returns

- **Type:** DremioConnection
- **Description:** A DremioConnection object configured for the specified mode.

**Raises**
- **ValueError**: Raised when:
Required environment variables for the specified mode are not set.
- An invalid mode is provided (anything other than "cloud" or "software").

## Required Environment Variables
The following variables must be defined in the env.py file or elsewhere in your environment:

| **Variable**       | **Required for Mode** | **Description**                                                                         |
|---------------------|-----------------------|-----------------------------------------------------------------------------------------|
| `DREMIO_TOKEN`      | Cloud                | Authentication token for Dremio Cloud.                                                 |
| `DREMIO_USERNAME`   | Software             | Username for Dremio Software authentication.                                           |
| `DREMIO_PASSWORD`   | Software             | Password for Dremio Software authentication.                                           |
| `DREMIO_URI`        | Both                 | The URI of the Dremio instance. For example: `grpc+tls://data.dremio.cloud:443`.       |
| `DREMIO_LOGIN_URI`  | Software             | The REST API endpoint for obtaining an authentication token for Dremio Software.       |


## Example Usage

#### Connecting to Dremio Cloud
```python
from dremio_connect import get_dremio_connection

# Connect to Dremio Cloud
dremio_connection = get_dremio_connection(mode="cloud")
print("Connected to Dremio Cloud!")
```
#### Connecting to Dremio Software
```python
from dremio_connect import get_dremio_connection

# Connect to Dremio Software
dremio_connection = get_dremio_connection(mode="software")
print("Connected to Dremio Software!")
```

## Code Walkthrough


### Mode: cloud

- Ensures that DREMIO_TOKEN and DREMIO_URI are set.
- Uses these credentials to directly create a DremioConnection object.

### Mode: software

- Ensures that DREMIO_LOGIN_URI, DREMIO_USERNAME, and DREMIO_PASSWORD are set.
- Fetches a token from the Dremio REST API by providing the username and password.
- Uses the fetched token to create a DremioConnection object.

## Error Handling

- Raises a ValueError if any required variables are missing for the chosen mode.
- Raises a ValueError if an invalid mode is provided.

## Notes
- **Security**: Ensure your `DREMIO_TOKEN`, `DREMIO_USERNAME`, and `DREMIO_PASSWORD` are stored securely and not hardcoded into your source code.

#### Dremio Cloud vs. Software:
- Use "cloud" mode for Dremio Cloud instances.
- Use "software" mode for self-hosted Dremio instances or enterprise deployments.

## Suggested Enhancements
- Add logging for debugging connection errors.
- Include token caching for the software mode to avoid frequent API calls for authentication.
- Add support for other configurations like custom SSL certificates or timeouts.

from dremio_simple_query.connect import DremioConnection, get_token
from env import DREMIO_TOKEN, DREMIO_USERNAME, DREMIO_PASSWORD, DREMIO_URI, DREMIO_LOGIN_URI

def get_dremio_connection(mode="software"):
    """
    Returns a DremioConnection object based on the mode ("cloud" or "software").
    
    Args:
        mode (str): "cloud" or "software" (default is "software").
        
    Returns:
        DremioConnection: A connection to Dremio based on the mode.
    """
    if mode == "cloud":
        # Use the token for Dremio Cloud
        if not DREMIO_TOKEN or not DREMIO_URI:
            raise ValueError("DREMIO_TOKEN and DREMIO_URI must be set for Dremio Cloud.")
        return DremioConnection(DREMIO_TOKEN, DREMIO_URI)
    elif mode == "software":
        # Fetch a token using username and password for Dremio Software
        if not DREMIO_LOGIN_URI or not DREMIO_USERNAME or not DREMIO_PASSWORD:
            raise ValueError("DREMIO_LOGIN_URI, DREMIO_USERNAME, and DREMIO_PASSWORD must be set for Dremio Software.")
        token = get_token(uri=DREMIO_LOGIN_URI, payload={
            "userName": DREMIO_USERNAME,
            "password": DREMIO_PASSWORD,
        })
        return DremioConnection(token, DREMIO_URI)
    else:
        raise ValueError("Invalid mode. Must be 'cloud' or 'software'.")

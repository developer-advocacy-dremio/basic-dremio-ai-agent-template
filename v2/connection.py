from dremio_simple_query.connect import DremioConnection, get_token
from langchain_community.llms import OpenAI
from os import getenv
from dotenv import load_dotenv
from DremioSQLDatabase import DremioSQLDatabase

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

# ✅ Initialize the Custom Database for LangChain
db = DremioSQLDatabase(dremio)

# ✅ Initialize OpenAI LLM
llm = OpenAI(model="gpt-3.5-turbo-instruct", temperature=0)




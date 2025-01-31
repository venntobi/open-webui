import logging
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import httpx

# http_client = httpx.Client(
#     verify=r"c:\\Users\\vennt\\Desktop\\Projekte\\00_Gitlab\\Öffentlich\\open-webui\\.venv\\Lib\\site-packages\\certifi\\cacert.pem"
# )


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_GPT")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY_GPT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION_GPT")
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT")

logger.debug("EINLESEN API VERSION: ", AZURE_OPENAI_API_VERSION)

client = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    # http_client=http_client,
)

response = client.chat.completions.create(model=MODEL, messages="Test Prompt")

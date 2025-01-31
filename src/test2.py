import logging
import requests
from dotenv import load_dotenv
import os
import json

# Logging einrichten
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Umgebungsvariablen laden
load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_GPT")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY_GPT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION_GPT")
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT")

logger.debug(f"EINLESEN API VERSION: {AZURE_OPENAI_API_VERSION}")

# URL für die API-Anfrage
url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{MODEL}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"

# Header und Payload definieren
headers = {"Content-Type": "application/json", "api-key": API_KEY}

payload = {"messages": [{"role": "user", "content": "Wie geht es dir?"}], "max_tokens": 100}

# Anfrage senden
try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    result = response.json()
    logger.debug(json.dumps(result, indent=4))
    print(result)
except requests.exceptions.RequestException as e:
    logger.error(f"Fehler bei der Anfrage: {e}")

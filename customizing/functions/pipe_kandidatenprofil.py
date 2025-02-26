"""
title: Azure OpenAI Pipe
author: open-webui, adapted by nomppy
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1.0
license: MIT
"""

# * Wichtige Funktion
# * Der Rest ist in:  backend\open_webui\static\templates\bludau

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import requests
import os
import docx
import PyPDF2


from backend.open_webui.static.prompts.system_prompt import SYSTEM_PROMPT


class Pipe:
    class Valves(BaseModel):
        # TODO: für openai-schnittstelle: env anpassen
        # TODO: url zusammenbau anpassen
        # TODO: Bei url muss o1 angesprochen werden
        # You can add your custom valves here.
        AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY_GPT", "API_KEY")
        AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT_GPT", "API_ENDPOINT")
        AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT", "DEPLOYMENT_NAME")
        AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION_GPT", "API_VERSION")

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "azure_openai_pipeline"
        # TODO: Umnennen zu Kandidatenprofil oder ähnlich
        self.name = "Kandidatenprofil_Azure"
        self.valves = self.Valves()
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        # Dies ist die zentrale Funktion, die am Ende
        # den Request an Azure OpenAI sendet.
        print(f"System Prompt von mir: {SYSTEM_PROMPT}")
        print(f"pipe:{__name__}")

        # System-Prompt als erste Nachricht an.
        if "messages" not in body:
            body["messages"] = []

        body["messages"].insert(0, {"role": "system", "content": SYSTEM_PROMPT})

        headers = {
            "api-key": self.valves.AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json",
        }
        # TODO: Hier url muss angepasst werden
        url = (
            f"{self.valves.AZURE_OPENAI_ENDPOINT}/openai/deployments/"
            f"{self.valves.AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions"
            f"?api-version={self.valves.AZURE_OPENAI_API_VERSION}"
        )

        # Nur diese Felder werden an die Azure-API weitergereicht
        allowed_params = {
            "messages",
            "temperature",
            "role",
            "content",
            "contentPart",
            "contentPartImage",
            "enhancements",
            "dataSources",
            "n",
            "stream",
            "stop",
            "max_tokens",
            "presence_penalty",
            "frequency_penalty",
            "logit_bias",
            "user",
            "function_call",
            "funcions",
            "tools",
            "tool_choice",
            "top_p",
            "log_probs",
            "top_logprobs",
            "response_format",
            "seed",
        }

        # remap user field (falls "user" kein String ist)
        if "user" in body and not isinstance(body["user"], str):
            body["user"] = body["user"]["id"] if "id" in body["user"] else str(body["user"])

        filtered_body = {k: v for k, v in body.items() if k in allowed_params}

        # Logge gefilterte Felder
        if len(body) != len(filtered_body):
            print(f"Dropped params: {', '.join(set(body.keys()) - set(filtered_body.keys()))}")
        r = None

        try:
            r = requests.post(
                url=url,
                json=filtered_body,
                headers=headers,
                stream=True,
                # response_format={"type": "json_object"},
            )
            r.raise_for_status()

            # Bei streaming=True werden die Antwortzeilen gestreamt
            if body.get("stream"):
                return r.iter_lines()
            else:
                return r.json()

        except Exception as e:
            print("Requests error in Azure pipeline")
            if "r" in locals() and r is not None:
                text = r.text
                return f"Error: {e} ({text})"
            else:
                return f"Error: {e}"

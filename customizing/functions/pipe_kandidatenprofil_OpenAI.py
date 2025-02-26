"""
title: OpenAI Proxy Pipe
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1.0
"""

from pydantic import BaseModel, Field
from typing import Optional, Union, Generator, Iterator

import os
import requests

from backend.open_webui.static.prompts.system_prompt import SYSTEM_PROMPT


class Pipe:
    class Valves(BaseModel):
        NAME_PREFIX: str = Field(
            default="OPENAI/",
            description="Prefix to be added before model names.",
        )
        OPENAI_API_BASE_URL: str = Field(
            default="https://api.openai.com/v1",
            description="Base URL for accessing OpenAI API endpoints.",
        )
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "API_KEY")
        pass

    def __init__(self):
        self.valves = self.Valves()
        pass

    def pipes(self):
        if self.valves.OPENAI_API_KEY:
            try:
                headers = {}
                headers["Authorization"] = f"Bearer {self.valves.OPENAI_API_KEY}"
                headers["Content-Type"] = "application/json"

                r = requests.get(f"{self.valves.OPENAI_API_BASE_URL}/models", headers=headers)

                models = r.json()
                return [
                    {
                        "id": model["id"],
                        "name": f'{self.valves.NAME_PREFIX}{model["name"] if "name" in model else model["id"]}',
                    }
                    for model in models["data"]
                    if "gpt" in model["id"]
                ]

            except Exception as e:

                print(f"Error: {e}")
                return [
                    {
                        "id": "error",
                        "name": "Could not fetch model, please update the API Key in the valves.",
                    },
                ]
        else:
            return [
                {
                    "id": "error",
                    "name": "API Key not provided.",
                },
            ]

    def pipe(self, body: dict, __user__: dict) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")
        headers = {}
        headers["Authorization"] = f"Bearer {self.valves.OPENAI_API_KEY}"
        headers["Content-Type"] = "application/json"
        if "messages" not in body:
            body["messages"] = []

        body["messages"].insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        model_id = body["model"][body["model"].find(".") + 1 :]
        payload = {**body, "model": model_id}

        try:
            r = requests.post(
                url=f"{self.valves.OPENAI_API_BASE_URL}/chat/completions",
                json=payload,
                headers=headers,
                stream=True,
            )

            r.raise_for_status()

            if body["stream"]:
                return r.iter_lines()
            else:
                return r.json()
        except Exception as e:
            return f"Error: {e}"

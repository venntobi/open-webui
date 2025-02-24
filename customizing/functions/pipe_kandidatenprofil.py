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


from open_webui.static.templates.word_context_template import (
    context as context_template,
)
from open_webui.static.templates.word_context_kandidat3 import (
    context as context_example,
)


# TODO: in externe Datei ausgliedern, z.B. backend.open_webui.utils.misc
def read_pdf_content(filepath: str) -> str:
    """
    Liest den Inhalt einer PDF-Datei ein und gibt ihn als String zurück.
    """
    text_content = []

    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        # Schleife durch alle Seiten
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            # Extrahiert den Text pro Seite
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)

    # Die einzelnen Seiten durch einen Zeilenumbruch trennen
    return "\n".join(text_content)


EXAMPLE_CV_PATH = os.path.join("backend", "open_webui", "static", "templates", "bludau", "CV.pdf")
EXAMPLE_REPORT_PATH = os.path.join("backend", "open_webui", "static", "templates", "bludau", "Report.pdf")
EXAMPLE_QUESTIONARE_PATH = os.path.join("backend", "open_webui", "static", "templates", "bludau", "Fragebogen.pdf")

cv = read_pdf_content(EXAMPLE_CV_PATH)
report = read_pdf_content(EXAMPLE_REPORT_PATH)
questionare = read_pdf_content(EXAMPLE_QUESTIONARE_PATH)

# -- SYSTEM PROMPT --
# ? Auslagern? Dann kann man besser anpassen
SYSTEM_PROMPT = f"""
Du bist ein Tool zur Analyse und Zusammenfassung von Lebensläufen und Fragebögen. Deine Aufgabe ist es, alle relevanten Informationen vollständig und strukturiert in einem festen JSON-Schema zusammenzufassen. Achte insbesondere auf die Vollständigkeit der beruflichen Erfahrung. Fehlende Informationen dürfen nicht erfunden werden, sondern müssen weggelassen werden.

Anweisungen:

    Extrahiere und strukturiere die Daten gemäß dem vorgegebenen JSON-Schema.
    Achte besonders auf die vollständige Erfassung der fachlichen Eignung.
    Halte dich exakt an das vorgegebene Format – keine zusätzlichen Erläuterungen, Kommentare oder Abweichungen.
    Falls eine Kategorie nicht im Lebenslauf oder Fragebogen vorhanden ist, lasse sie weg, aber ändere nicht die Struktur des Outputs.

Ausgabe:
Dein Output muss genau diesem JSON-Schema entsprechen:
{context_template}. 
Jede generierte Ausgabe muss genau diesem Schema folgen, ohne zusätzlichen Text oder Erklärungen.

Hier ist ein Beispiel aus Dateien, die du bekommst und wie das Endergebnis aussehen muss:
Beispieldatei 1: {cv}
Beispieldatei 2: {report}
Beispieldatei 3: {questionare}

Ergebnis: {context_example}
"""


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
        self.name = "Azure OpenAI Pipe"
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

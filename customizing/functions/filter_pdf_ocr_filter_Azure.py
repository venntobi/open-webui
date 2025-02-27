from typing import Optional
import os
import io
from PIL import Image as PILImage
import numpy as np
import base64
from pdf2image import convert_from_path
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI


class Filter:
    def __init__(
        self,
        model_version=os.getenv("AZURE_OPENAI_API_VERSION_GPT", "API_VERSION"),
        model_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT_GPT", "API_ENDPOINT"),
        model_deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME_GPT", "DEPLOYMENT_NAME"),
        model_api_key=os.getenv("AZURE_OPENAI_API_KEY_GPT", "API_KEY"),
    ):
        self.model_available = False
        self.model_version = model_version
        self.model_endpoint = model_endpoint
        self.model_deployment_name = model_deployment_name
        self.model_api_key = model_api_key
        self.setup_model()

    def setup_model(self):
        self.model = AzureChatOpenAI(
            openai_api_key=self.model_api_key,
            azure_endpoint=self.model_endpoint,
            azure_deployment=self.model_deployment_name,
            openai_api_version=self.model_version,
            max_tokens=2000,
        )
        self.model_available = True

    def ocr_gptvision(self, file_path):
        self.setup_model()
        data_type = os.path.splitext(file_path)[1].lower()

        if data_type == ".pdf":
            print("Processing PDF with Azure OpenAI...")
            images = convert_from_path(file_path, dpi=72, first_page=1, last_page=10)
            extracted_text = ""

            for img_page in images:
                text = self.azure_vision_ocr(img_page)
                extracted_text += text

        return extracted_text

    def image_to_b64(self, pil_img):
        if pil_img.mode == "RGBA":
            pil_img = pil_img.convert("RGB")

        img_array = np.array(pil_img)

        with io.BytesIO() as buffer:
            PILImage.fromarray(img_array).save(buffer, format="JPEG")
            base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return base64_image

    def generate_prompt(self, input_image):
        messages = [
            SystemMessage(
                content="""
                    Du bist ein Bot, der beim Transkribieren von Bildern hilft. Deine Ausgabe soll aus exakt ein Objekt bestehen, das als Ausgabe für eine Python Funktion dient. \
                    Das Objekt ist ein String. \
                    Der String ist dabei der Text, den du aus einem Bild extrahieren sollst. \
                    Wenn es sich um ein Bild mit Text handelt, transkribiere den Text und beschreibe, was auf dem Bild zu sehen ist. Wenn es keinen Text gibt, beschreibe, was auf dem Bild zu sehen ist. \
                    Gib keine Überschrift oder Titel an und kommentiere deine Transkription nicht. Klassifiziere den Text nicht. \
                    Wenn du den Verdacht hast, dass das Bild oder der Text urheberrechtlich geschützt sein könnte, Verweigere in solchen Fällen NUR IM ABSOLUTEN AUSNAHMEFALL bei erheblichem Verdacht auf Urheberrechtsprobleme die Transkription oder Bildbeschreibung. Ist das nicht der Fall, transkribiere und beschreibe wie gewohnt. \
                """,
            ),
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{input_image}",
                        },
                    }
                ]
            ),
        ]

        return messages

    def azure_vision_ocr(self, input_text_or_image):
        base64_image = self.image_to_b64(input_text_or_image)
        messages = self.generate_prompt(base64_image)
        try:
            ai_answer = self.model.invoke(messages)
            answer = ai_answer.content
        except Exception as e:
            raise e

        return answer

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Pre-process the input data before sending it to the LLM.
        If any PDF files are detected, convert them to images and extract text using OCR.
        The extracted text will replace the original content in the file['file']['data']['content'].
        """

        # Check if there are any files and process all PDFs
        for file in body["files"]:
            filename = file["file"].get("filename", "")
            file_id = file["file"]["id"]

            if filename.lower().endswith(".pdf"):  # Check if the file is a PDF
                try:
                    # Construct the full path to the PDF file
                    pdf_path = f"backend/data/uploads/{file_id}_{filename}"

                    if not os.path.exists(pdf_path):
                        print(f"PDF file not found: {pdf_path}")
                        continue

                    # Convert the PDF pages to images and extract text
                    try:
                        extracted_text = self.ocr_gptvision(pdf_path)
                    except Exception as e:
                        print(f"Error converting PDF to images: {e}")

                    # Replace the file's content with the extracted text
                    file["file"]["data"]["content"] = extracted_text

                except Exception as e:
                    print(f"Error processing PDF {filename}: {e}")
        print("F", body["files"])
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Post-process the output data after receiving it from the LLM.
        This function can be used for additional modifications if needed.
        """
        return body

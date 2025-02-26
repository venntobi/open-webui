from io import BytesIO
from pathlib import Path
from typing import Dict, Any, List
from docxtpl import DocxTemplate
from open_webui.models.chats import ChatTitleMessagesForm
import ast
import json
import re

# from open_webui.routers.knowledge import get_knowledge_by_id
TEMPLATE_PATH = Path(__file__).parent.parent / "static" / "templates" / "bludau" / "template.docx"


class ChatWordGenerator:
    """
    Description:
    The `ChatWordGenerator` class is designed to create Word (.docx) documents by replacing placeholders
    in a template with chat message data.

    Attributes:
    - `form_data`: An instance of `ChatTitleMessagesForm` containing title and messages.
    """

    def __init__(self, form_data: ChatTitleMessagesForm):
        self.form_data = form_data

    def generate_chat_word(self) -> bytes:
        """
        Generate a Word document from a template and replace placeholders with chat message data.

        Returns:
        - The generated Word document as bytes.
        """
        try:
            string_response = self.form_data.messages[-1].get("content", "")
            match = re.search(r"\{.*\}", string_response, re.DOTALL)
            if match:
                string_response = match.group(0)
            context = ast.literal_eval(string_response)
            # Load the template document
            doc = DocxTemplate(TEMPLATE_PATH)
            doc.render(context)

            # Save the document to BytesIO
            word_io = BytesIO()
            doc.save(word_io)
            word_io.seek(0)
            return word_io.getvalue()
        except Exception as e:
            raise e

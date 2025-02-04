from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, List

from docx import Document
from open_webui.models.chats import ChatTitleMessagesForm


TEMPLATE_PATH = Path("backend/open_webui/static/templates/candidate_template.docx")


class ChatWordGenerator:
    """
    Description:
    The `WordGenerator` class is designed to create Word (.docx) documents from chat messages.

    Attributes:
    - `form_data`: An instance of `ChatTitleMessagesForm` containing title and messages.
    """

    def __init__(self, form_data: ChatTitleMessagesForm):
        self.form_data = form_data

    def _build_message_text(self, message: Dict[str, Any]) -> str:
        """Format a single message for the Word document."""
        content = message.get("content", "")

        return f"{content}"

    def generate_chat_word(self) -> bytes:
        """
        Generate a Word document from a template and fill it with chat messages.
        """
        try:

            doc = Document(TEMPLATE_PATH)

            # Add Message
            for msg in self.form_data.messages:
                doc.add_paragraph(self._build_message_text(msg))

            # Save document to BytesIO
            word_io = BytesIO()
            doc.save(word_io)
            word_io.seek(0)

            return word_io.getvalue()
        except Exception as e:
            raise e

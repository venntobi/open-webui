from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Dict, Any, List

from docx import Document
from open_webui.models.chats import ChatTitleMessagesForm


class WordGenerator:
    """
    Description:
    The `WordGenerator` class is designed to create Word (.docx) documents from chat messages.

    Attributes:
    - `form_data`: An instance of `ChatTitleMessagesForm` containing title and messages.
    """

    def __init__(self, form_data: ChatTitleMessagesForm):
        self.form_data = form_data

    def format_timestamp(self, timestamp: float) -> str:
        """Convert a UNIX timestamp to a formatted date string."""
        try:
            date_time = datetime.fromtimestamp(timestamp)
            return date_time.strftime("%Y-%m-%d, %H:%M:%S")
        except (ValueError, TypeError):
            return ""

    def _build_message_text(self, message: Dict[str, Any]) -> str:
        """Format a single message for the Word document."""
        role = message.get("role", "User").title()
        content = message.get("content", "")
        timestamp = message.get("timestamp")
        model = f" ({message.get('model')})" if message.get("model") and role == "Assistant" else ""

        date_str = self.format_timestamp(timestamp) if timestamp else ""

        return f"{role}{model} - {date_str}\n{content}\n"

    def generate_chat_word(self) -> bytes:
        """
        Generate a Word (.docx) file from chat messages.
        """
        try:
            doc = Document()

            # Add Title
            doc.add_heading(self.form_data.title, level=1)

            # Add Messages
            for msg in self.form_data.messages:
                doc.add_paragraph(self._build_message_text(msg))
                doc.add_paragraph("-" * 40)  # Separator

            # Save document to BytesIO
            word_io = BytesIO()
            doc.save(word_io)
            word_io.seek(0)

            return word_io.getvalue()
        except Exception as e:
            raise e

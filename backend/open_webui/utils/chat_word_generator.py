from io import BytesIO
from pathlib import Path
from typing import Dict, Any, List
from docx import Document
from docx.shared import Cm
from open_webui.models.chats import ChatTitleMessagesForm

TEMPLATE_PATH = Path("backend/open_webui/static/templates/Vorlage Kandidatenprofil_Farina.docx")


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

    def _extract_key_value_pairs(self, messages: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Extract key-value pairs from the messages where keys are bolded (e.g., **Kandidat**).

        Args:
        - `messages`: List of message dictionaries containing 'content'.

        Returns:
        - A dictionary mapping placeholder keys to their corresponding values.
        """
        key_value_pairs = {}
        for msg in messages:
            content = msg.get("content", "")
            lines = content.split("\n")
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("**") and line.endswith(":**"):
                    # Extract the key
                    key = line.strip("**:").strip()
                    # Find the next non-empty line as the value
                    value = ""
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines):
                        value = lines[j].strip()
                    # Add the key-value pair to the dictionary
                    key_value_pairs[key] = value
                    i = j  # Skip to the next line after the value
                else:
                    i += 1  # Move to the next line

        return key_value_pairs

    def _replace_placeholders_in_document(self, doc: Document, replacements: Dict[str, str]):
        """
        Replace placeholders in the Word document with the provided values.

        Args:
        - `doc`: The Document object to modify.
        - `replacements`: A dictionary mapping placeholder keys to their replacement values.
        """
        for paragraph in doc.paragraphs:
            for key, value in replacements.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, value)
                    paragraph.alignment = 0

        foto_placeholder = "{{FOTO}}"
        foto_path = Path("backend/open_webui/static/templates/Bewerbungsfoto.png")
        foto_width = Cm(4)
        foto_height = Cm(3)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in replacements.items():
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in cell.text:
                            # Replace the placeholder with the value
                            cell.text = cell.text.replace(placeholder, value)
                            # Align the text to the left
                            for paragraph in cell.paragraphs:
                                paragraph.alignment = 0  # 0 corresponds to WD_ALIGN_PARAGRAPH.LEFT
                    if foto_placeholder in cell.text:
                        # Clear the cell's content
                        for paragraph in cell.paragraphs:
                            paragraph.clear()

                        # Add the image to the cell
                        cell.paragraphs[0].add_run().add_picture(str(foto_path), width=foto_width, height=foto_height)

    def generate_chat_word(self) -> bytes:
        """
        Generate a Word document from a template and replace placeholders with chat message data.

        Returns:
        - The generated Word document as bytes.
        """
        try:
            # Load the template document
            doc = Document(TEMPLATE_PATH)

            # Extract key-value pairs from the messages
            key_value_pairs = self._extract_key_value_pairs(self.form_data.messages)

            # Replace placeholders in the document
            self._replace_placeholders_in_document(doc, key_value_pairs)

            # Save the document to BytesIO
            word_io = BytesIO()
            doc.save(word_io)
            word_io.seek(0)

            return word_io.getvalue()
        except Exception as e:
            raise e

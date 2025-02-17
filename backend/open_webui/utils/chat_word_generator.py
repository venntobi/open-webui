from io import BytesIO
from pathlib import Path
from typing import Dict, Any, List
import re
from docx import Document
from docx.shared import Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt
from open_webui.models.chats import ChatTitleMessagesForm


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
        Extract key-value pairs from the messages where keys are capitalized (e.g., KANDIDAT).
        Handles multi-line values by preserving line breaks and stopping at the next key.

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
                if line.isupper():
                    key = line.strip(":").strip()
                    value_lines = []
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j].strip()
                        if next_line.isupper():
                            break
                        if next_line != "":
                            value_lines.append(next_line)
                        j += 1
                    value = "\n".join(value_lines)
                    key_value_pairs[key] = value
                    i = j
                else:
                    i += 1
        return key_value_pairs

    def _extract_contact_person_value(self, key_value_pairs: Dict[str, str]):
        """
        Extract contact person by extracting the value of the key "Ansprechpartner".

        Args:
        - `key_value_pairs`: dictionary containing the key value pairs.

        Returns:
        - A path of the document template as string.
        """
        for key, value in key_value_pairs.items():
            if key == "ANSPRECHPARTNER":
                if "Farina" in value:
                    path = (
                        Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Farina.docx"
                    )
                elif "Zoe" in value:
                    path = Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Zoe.docx"
                elif "Yasemin" in value:
                    path = (
                        Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Yasemin.docx"
                    )
                elif "Viktoria" in value:
                    path = (
                        Path(__file__).parent.parent
                        / "static"
                        / "templates"
                        / "Vorlage Kandidatenprofil_Viktoria.docx"
                    )
                elif "Tina" in value:
                    path = Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Tina.docx"
                elif "Stephan" in value:
                    path = (
                        Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Stephan.docx"
                    )
                elif "Maike" in value:
                    path = (
                        Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Maike.docx"
                    )
                elif "Lucas" in value:
                    path = (
                        Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Lucas.docx"
                    )
                elif "Fynn" in value:
                    path = Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Fynn.docx"
                else:
                    path = Path(__file__).parent.parent / "static" / "templates" / "Vorlage Kandidatenprofil_Kaan.docx"
        return path

    def _replace_placeholders_in_document(self, doc: Document, replacements: Dict[str, str]):
        """
        Replace placeholders in the Word document with the provided values.

        Args:
        - `doc`: The Document object to modify.
        - `replacements`: A dictionary mapping placeholder keys to their replacement values.
        """
        center_aligned_placeholders = {"UNTERNEHMEN", "POSITION"}
        bold_placeholders = {"KANDIDAT", "AKTUELLE POSITION"}
        background_placeholders = {
            "BERUFLICHER WERDEGANG",
            "TÄTIGKEITEN WÄHREND DES STUDIUMS",
            "AKADEMISCHE AUSBILDUNG",
            "BERUFSAUSBILDUNG",
            "ZIVILDIENST",
            "SCHULISCHE AUSBILDUNG",
        }

        def format_background(value):
            """Format the value of  background."""
            if re.match(r"^\d", value):  # First letter is a number
                lines = value.split("\n")
                formatted_lines = []
                for line in lines:
                    if re.match(r"^\d", line):  # First letter is a number
                        match = re.match(r"^([\d/]+(?:\s*-\s*(?:[\d/]+|heute))?)\s*(.*)", line)
                        if match:
                            line_1 = match.group(1)
                            line_2 = match.group(2)
                        formatted_line = line_1.strip() + "\t\t\t" + line_2.strip()
                        formatted_lines.append(formatted_line)
                    else:
                        if len(line) < 70:
                            if line.strip().startswith("•"):
                                formatted_line = "\t\t\t\t           " + line[1:].strip()
                                formatted_lines.append(formatted_line)
                            else:
                                formatted_line = "\t\t\t\t" + line.strip()
                                formatted_lines.append(formatted_line)
                        if len(line) > 70 and len(line) < 140:
                            if line.strip().startswith("•"):
                                formatted_line_1 = "\t\t\t\t           " + line[1:70].strip() + "-"
                                formatted_line_2 = "\t\t\t\t              " + line[70:].strip()
                                formatted_lines.append(formatted_line_1)
                                formatted_lines.append(formatted_line_2)
                            else:
                                formatted_line_1 = "\t\t\t\t" + line.strip()[:70].strip() + "-"
                                formatted_line_2 = "\t\t\t\t" + line.strip()[70:].strip()
                                formatted_lines.append(formatted_line_1)
                                formatted_lines.append(formatted_line_2)
                        if len(line) > 140 and len(line) < 210:
                            formatted_line_1 = "\t\t\t\t" + line.strip()[:70].strip() + "-"
                            formatted_line_2 = "\t\t\t\t" + line.strip()[70:140].strip() + "-"
                            formatted_line_3 = "\t\t\t\t" + line.strip()[140:].strip()
                            formatted_lines.append(formatted_line_1)
                            formatted_lines.append(formatted_line_2)
                            formatted_lines.append(formatted_line_3)
                        if len(line) > 210 and len(line) < 280:
                            formatted_line_1 = "\t\t\t\t" + line.strip()[:70].strip() + "-"
                            formatted_line_2 = "\t\t\t\t" + line.strip()[70:140].strip() + "-"
                            formatted_line_3 = "\t\t\t\t" + line.strip()[140:210].strip() + "-"
                            formatted_line_4 = "\t\t\t\t" + line.strip()[210:].strip()
                            formatted_lines.append(formatted_line_1)
                            formatted_lines.append(formatted_line_2)
                            formatted_lines.append(formatted_line_3)
                            formatted_lines.append(formatted_line_4)
                        if len(line) > 280:
                            formatted_line_1 = "\t\t\t\t" + line.strip()[:70].strip() + "-"
                            formatted_line_2 = "\t\t\t\t" + line.strip()[70:140].strip() + "-"
                            formatted_line_3 = "\t\t\t\t" + line.strip()[140:210].strip() + "-"
                            formatted_line_4 = "\t\t\t\t" + line.strip()[210:280].strip() + "-"
                            formatted_line_5 = "\t\t\t\t" + line.strip()[280:].strip()
                            formatted_lines.append(formatted_line_1)
                            formatted_lines.append(formatted_line_2)
                            formatted_lines.append(formatted_line_3)
                            formatted_lines.append(formatted_line_4)
                            formatted_lines.append(formatted_line_5)
                return "\n".join(formatted_lines)
            else:
                return value

        def format_bullet_points(value):
            """Format the value to replace placeholders with proper bullet points and indentation."""
            lines = value.split("\n")
            formatted_lines = []
            for line in lines:
                if line.strip().startswith("•"):
                    if len(line) < 100:
                        formatted_line = "        •  " + line[1:].strip()
                        formatted_lines.append(formatted_line)
                    if len(line) > 100 and len(line) < 180:
                        formatted_line_1 = "        •  " + line.strip()[1:90].strip() + "-"
                        formatted_line_2 = "           " + line.strip()[90:].strip()
                        formatted_lines.append(formatted_line_1)
                        formatted_lines.append(formatted_line_2)
                    elif len(line) > 180:
                        formatted_line_1 = "        •  " + line.strip()[1:90].strip() + "-"
                        formatted_line_2 = "           " + line.strip()[90:180].strip() + "-"
                        formatted_line_3 = "           " + line.strip()[180:].strip()
                        formatted_lines.append(formatted_line_1)
                        formatted_lines.append(formatted_line_2)
                        formatted_lines.append(formatted_line_3)
                elif line.strip().startswith("◦"):
                    if len(line) < 90:
                        formatted_line = "\t       ◦  " + line[1:].strip()
                        formatted_lines.append(formatted_line)
                    if len(line) > 90 and len(line) < 160:
                        formatted_line_1 = "\t       ◦  " + line.strip()[1:80].strip() + "-"
                        formatted_line_2 = "\t          " + line.strip()[80:].strip()
                        formatted_lines.append(formatted_line_1)
                        formatted_lines.append(formatted_line_2)
                    elif len(line) > 160:
                        formatted_line_1 = "\t       ◦  " + line.strip()[1:80].strip() + "-"
                        formatted_line_2 = "\t          " + line.strip()[80:160].strip() + "-"
                        formatted_line_3 = "\t          " + line.strip()[160:].strip()
                        formatted_lines.append(formatted_line_1)
                        formatted_lines.append(formatted_line_2)
                        formatted_lines.append(formatted_line_3)
                else:
                    formatted_lines.append(line)
            return "\n".join(formatted_lines)

        for paragraph in doc.paragraphs:
            for key, value in replacements.items():
                formatted_value = format_bullet_points(value)
                if key in background_placeholders:
                    formatted_value = format_background(formatted_value)
                placeholder = f"{{{{{key}}}}}"
                if placeholder in paragraph.text:
                    paragraph.text = paragraph.text.replace(placeholder, formatted_value)
                    if key in background_placeholders:
                        if re.match(r"^\d", value):
                            paragraph_text = paragraph.text.strip()
                            lines = paragraph_text.split("\n")
                            if lines:
                                paragraph.clear()
                                # Add first line with bold formatting
                                first_run = paragraph.add_run(lines[0] + "\n")
                                first_run.bold = True
                                # Add the rest of the paragraph without bold
                                for line in lines[1:]:
                                    paragraph.add_run(line + "\n")
                    if key in center_aligned_placeholders:
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
                        for run in paragraph.runs:
                            run.font.name = "Arial"
                            run.font.size = Pt(12)
                    else:
                        paragraph.alignment = 0
                        paragraph.paragraph_format.line_spacing = 1.15
                        for run in paragraph.runs:
                            run.font.name = "Arial"
                            run.font.size = Pt(10)

        foto_placeholder = "{{FOTO}}"
        foto_path = Path(__file__).parent.parent / "static" / "templates" / "Bewerbungsfoto.png"
        foto_width = Cm(4)
        foto_height = Cm(3)

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in replacements.items():
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in cell.text:
                            cell.text = cell.text.replace(placeholder, value)
                            for paragraph in cell.paragraphs:
                                paragraph.alignment = 0
                                if key in bold_placeholders:
                                    for run in paragraph.runs:
                                        if value in run.text:
                                            run.text = run.text.replace(value, "")
                                            new_run = paragraph.add_run(value)
                                            new_run.bold = True
                                            new_run.font.name = "Arial"
                                            new_run.font.size = Pt(10)
                                        else:
                                            run.font.name = "Arial"
                                            run.font.size = Pt(10)

                    if foto_placeholder in cell.text:
                        for paragraph in cell.paragraphs:
                            paragraph.clear()

                        cell.paragraphs[0].add_run().add_picture(str(foto_path), width=foto_width, height=foto_height)

    # Step 2: Remove any remaining placeholders (not replaced by values)
    def _remove_remaining_placeholders(self, doc):
        """remove any remaining placeholders in doc"""
        placeholder_pattern = re.compile(r"\{\{.*?\}\}")

        for paragraph in doc.paragraphs:
            matches = placeholder_pattern.findall(paragraph.text)
            if matches:
                for match in matches:
                    paragraph.text = paragraph.text.replace(match, "")

        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    matches = placeholder_pattern.findall(cell.text)
                    if matches:
                        for match in matches:
                            cell.text = cell.text.replace(match, "")

    def generate_chat_word(self) -> bytes:
        """
        Generate a Word document from a template and replace placeholders with chat message data.

        Returns:
        - The generated Word document as bytes.
        """
        try:
            # Extract key-value pairs from the messages
            key_value_pairs = self._extract_key_value_pairs(self.form_data.messages)

            # Extract contact person from the messages
            path = self._extract_contact_person_value(key_value_pairs)

            # Load the template document
            doc = Document(path)

            # Replace placeholders in the document
            self._replace_placeholders_in_document(doc, key_value_pairs)

            # Replace remaining placeholders with empty string
            self._remove_remaining_placeholders(doc)

            # Save the document to BytesIO
            word_io = BytesIO()
            doc.save(word_io)
            word_io.seek(0)

            return word_io.getvalue()
        except Exception as e:
            raise e

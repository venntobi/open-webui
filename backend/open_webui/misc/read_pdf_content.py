import PyPDF2


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

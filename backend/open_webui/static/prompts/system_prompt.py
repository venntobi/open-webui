import os

from backend.open_webui.static.templates.word_context_template import (
    context as context_template,
)
from backend.open_webui.static.templates.word_context_kandidat3 import (
    context as context_example,
)
from backend.open_webui.misc.read_pdf_content import read_pdf_content

EXAMPLE_CV_PATH = os.path.join("backend", "open_webui", "static", "templates", "bludau", "CV.pdf")
EXAMPLE_REPORT_PATH = os.path.join("backend", "open_webui", "static", "templates", "bludau", "Report.pdf")
EXAMPLE_QUESTIONARE_PATH = os.path.join("backend", "open_webui", "static", "templates", "bludau", "Fragebogen.pdf")

cv = read_pdf_content(EXAMPLE_CV_PATH)
report = read_pdf_content(EXAMPLE_REPORT_PATH)
questionare = read_pdf_content(EXAMPLE_QUESTIONARE_PATH)

# -- SYSTEM PROMPT --
SYSTEM_PROMPT = f"""
Du bist ein Tool zur Analyse und Zusammenfassung von Lebensläufen und Fragebögen. Deine Aufgabe ist es, alle relevanten Informationen vollständig und strukturiert in einem festen JSON-Schema zusammenzufassen. Achte insbesondere auf die Vollständigkeit der beruflichen Erfahrung. Fehlende Informationen dürfen nicht erfunden werden, sondern müssen mit '' ersetzt werden.

Anweisungen:

    Extrahiere und strukturiere die Daten gemäß dem vorgegebenen JSON-Schema.
    Achte besonders auf die vollständige Erfassung der fachlichen Eignung.
    Halte dich exakt an das vorgegebene Format – keine zusätzlichen Erläuterungen, Kommentare oder Abweichungen.
    Falls eine Kategorie nicht im Lebenslauf oder Fragebogen vorhanden ist, lasse sie weg, und ersetze sie mit '' anstelle von Ellipsen (`...`), aber ändere nicht die Struktur des Outputs.

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

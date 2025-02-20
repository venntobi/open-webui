from docxtpl import DocxTemplate
from word_context import context


def render():
    doc = DocxTemplate(r"customizing\Kandidatenprofil_Vorlage.docx")
    doc.render(context)
    doc.save(r"customizing\Kandidatenprofil_Vorlage_Test.docx")

from fpdf import FPDF
import tempfile

class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)  # Download font if missing
        self.set_font("DejaVu", size=12)

    def add_text(self, text):
        self.add_page()
        self.multi_cell(0, 10, text)

def export_chat_to_pdf(chat_history):
    pdf = UnicodePDF()
    combined = ""
    for sender, msg in chat_history:
        combined += f"{sender}: {msg}\n\n"

    pdf.add_text(combined)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

import io
import re
import pdfplumber
import spacy

nlp = spacy.load("pt_core_news_sm")

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_email_text(text: str) -> str:
    # Preserve original case for date/time detection
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and (token.is_alpha or token.is_digit or token.text in ['h', ':', '/', '-'])]
    return " ".join(tokens)


# Adiciona tratamento de erro ao extrair texto do PDF
def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return clean_text(text)
    except Exception as e:
        raise ValueError(f"Erro ao extrair texto do PDF: {str(e)}")

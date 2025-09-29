import io
import re
import pdfplumber
import spacy

# Carrega o modelo spaCy com tratamento de erro
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback: baixa o modelo se não estiver disponível
    try:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    except:
        # Último recurso: cria um modelo básico sem funcionalidades avançadas
        nlp = None

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def preprocess_email_text(text: str) -> str:
    # Se o modelo spaCy não estiver disponível, retorna o texto limpo
    if nlp is None:
        return clean_text(text)

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
            return clean_text(text) if text.strip() else ""
    except Exception as e:
        # Tenta método alternativo com PyPDF2 se pdfplumber falhar
        try:
            from PyPDF2 import PdfReader
            with io.BytesIO(pdf_bytes) as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return clean_text(text) if text.strip() else ""
        except Exception as e2:
            raise ValueError(f"Erro ao extrair texto do PDF (pdfplumber: {str(e)}, PyPDF2: {str(e2)})")

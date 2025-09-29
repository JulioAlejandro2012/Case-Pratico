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
    print(f"Extraindo texto de PDF com {len(pdf_bytes)} bytes")
    try:
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            print(f"PDF tem {len(pdf.pages)} páginas")
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                print(f"Página {i+1}: {len(page_text) if page_text else 0} caracteres")
                if page_text:
                    text += page_text + "\n"
            result = clean_text(text) if text.strip() else ""
            print(f"Texto final extraído: {len(result)} caracteres")
            return result
    except Exception as e:
        print(f"Erro com pdfplumber: {str(e)}")
        # Tenta método alternativo com PyPDF2 se pdfplumber falhar
        try:
            from PyPDF2 import PdfReader
            print("Tentando com PyPDF2...")
            with io.BytesIO(pdf_bytes) as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                print(f"PyPDF2 encontrou {len(pdf_reader.pages)} páginas")
                text = ""
                for i, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    print(f"PyPDF2 Página {i+1}: {len(page_text) if page_text else 0} caracteres")
                    text += page_text + "\n"
                result = clean_text(text) if text.strip() else ""
                print(f"Texto final com PyPDF2: {len(result)} caracteres")
                return result
        except Exception as e2:
            print(f"Erro com PyPDF2: {str(e2)}")
            raise ValueError(f"Erro ao extrair texto do PDF (pdfplumber: {str(e)}, PyPDF2: {str(e2)})")

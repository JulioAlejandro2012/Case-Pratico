import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from backend.nlp import preprocess_email_text

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Defina a variável de GEMINI_API_KEY no ambiente.")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY
)

classification_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente que classifica emails em apenas duas categorias: "
     "'Produtivo' ou 'Improdutivo'."),
    ("human", "Email:\n{email_text}\n\nResponda apenas com a categoria.")
])

response_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente que sugere respostas automáticas para emails corporativos.\n"
     "Seu tom deve ser educado, formal, cordial e profissional."),
    ("human",
     "Email:\n{email_text}\n\n"
     "Categoria: {categoria}\n"
     "Sugira uma resposta adequada seguindo o padrão de email corporativo formal.")
])

def classify_email(email_text: str) -> str:
    chain = classification_prompt | model
    result = chain.invoke({"email_text": email_text})
    return result.content.strip()

def generate_response(email_text: str, categoria: str) -> str:
    chain = response_prompt | model
    result = chain.invoke({"email_text": email_text, "categoria": categoria})
    return result.content.strip()

def process_email(raw_text: str) -> dict:
    clean_text = preprocess_email_text(raw_text)
    categoria = classify_email(clean_text)
    resposta = generate_response(clean_text, categoria)

    return {
        "Categoria": categoria,
        "Resposta": resposta
    }
import os
from datetime import datetime
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.tools.file_management import ReadFileTool, FileSearchTool, ListDirectoryTool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools.file_management import ReadFileTool
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.tools import tool
from backend.nlp import preprocess_email_text

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Defina a variável de GEMINI_API_KEY no ambiente.")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=GEMINI_API_KEY
)

# Inicializa ferramentas com tratamento de erro
try:
    agent_tools = [ReadFileTool(), FileSearchTool(), ListDirectoryTool()]
except Exception as e:
    # Fallback para ferramentas básicas se houver erro
    agent_tools = []

# Prompt para classificação
classification_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    Você é um assistente que classifica e-mails corporativos.

    INSTRUÇÕES DE CLASSIFICAÇÃO:
    - Classifique APENAS como "Produtivo" ou "Improdutivo"
    - Produtivo: E-mails profissionais, solicitações de trabalho, alinhamentos, reuniões, entregas, feedbacks, informações relevantes para o negócio
    - Improdutivo: E-mails pessoais, correntes, propagandas, spam, assuntos não relacionados ao trabalho, fofocas, mensagens irrelevantes ou mensagens de baixo calão

    Retorne APENAS a classificação: "Produtivo" ou "Improdutivo"
    """),
    ("human","Classifique este e-mail: {email_text}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Prompt para resposta
response_prompt = ChatPromptTemplate.from_messages([
    ("system","""
    Você é um assistente que gera respostas automáticas para e-mails corporativos.

    INSTRUÇÕES PARA RESPOSTA:
    - SEMPRE responda no formato de um e-mail, não importa o conteúdo da mensagem
    - SEMPRE acesse ./rules.md para obter as regras e exemplos de respostas
    - SEMPRE responda de forma educada, formal, cordial e profissional
    - SEMPRE responda de forma coerente e relevante ao conteúdo do e-mail:
        - Se algo não fizer sentido, peça esclarecimentos
        - Se for um e-mail pessoal, responda de forma educada, mas informe que não pode ajudar
        - Lide de forma apropriada com e-mails de spam, propaganda ou com conteúdo inadequado
    - Você DEVE usar saudações apropriadas
    - Você DEVE ser objetivo e claro
    - Você DEVE seguir os exemplos do arquivo ./rules.md
    - Você NÃO DEVE utilizar gírias ou abreviações informais
    - Você DEVE terminar com despedida formal (Atenciosamente, Cordialmente)
    """),
    ("human","""
    Gere uma resposta para este e-mail seguindo o padrão corporativo formal.
    Email: {email_text}
    """),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Agent para classificação
classification_agent = create_tool_calling_agent(model, agent_tools, classification_prompt)
classification_executor = AgentExecutor(agent=classification_agent, tools=agent_tools, verbose=False)

# Agent para resposta
response_agent = create_tool_calling_agent(model, agent_tools, response_prompt)
response_executor = AgentExecutor(agent=response_agent, tools=agent_tools, verbose=False)

def generate_classification(email_text: str) -> str:
    """Gera apenas a classificação do e-mail"""
    result = classification_executor.invoke({"email_text": email_text})
    classification = result["output"].strip()
    # Garante que seja apenas Produtivo ou Improdutivo
    if "Produtivo" in classification:
        return "Produtivo"
    else:
        return "Improdutivo"

def generate_response(email_text: str) -> str:
    """Gera apenas a resposta do e-mail"""
    result = response_executor.invoke({"email_text": email_text})
    return result["output"].strip()

def process_email(raw_text: str) -> dict:
    try:
        print(f"Processando e-mail com {len(raw_text)} caracteres")
        clean_text = preprocess_email_text(raw_text)
        print(f"Texto limpo: {len(clean_text)} caracteres")

        classification = generate_classification(clean_text)
        print(f"Classificação: {classification}")

        response = generate_response(clean_text)
        print(f"Resposta gerada: {len(response)} caracteres")

        return {
            "response": response,
            "classification": classification
        }
    except Exception as e:
        print(f"Erro no process_email: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

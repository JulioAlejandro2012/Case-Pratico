from fastapi import FastAPI, UploadFile, Form, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.nlp import extract_text_from_pdf_bytes
from backend.agent import process_email
import uvicorn
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint
@app.post("/process-email/")
async def process_email_endpoint(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        email_text = ""
        if file:
            print(f"Processando arquivo: {file.filename}")
            if file.filename.endswith(".pdf"):
                contents = await file.read()
                print(f"Tamanho do PDF: {len(contents)} bytes")
                email_text = extract_text_from_pdf_bytes(contents)
                print(f"Texto extraído do PDF: {len(email_text)} caracteres")
            elif file.filename.endswith(".txt"):
                contents = await file.read()
                try:
                    email_text = contents.decode("utf-8")
                except UnicodeDecodeError:
                    raise HTTPException(status_code=400, detail="Não foi possível decodificar o arquivo TXT. " \
                    "Verifique se ele está em formato UTF-8.")
            else:
                raise HTTPException(status_code=415, detail="Formato de arquivo não suportado. Use .txt ou .pdf.")
        elif text:
            email_text = text
        else:
            raise HTTPException(status_code=400, detail="Nenhum texto ou arquivo foi enviado.")

        print(f"Texto para processar: {email_text[:100]}...")

        # Utiliza a função centralizada do agent.py
        result = process_email(email_text)
        print(f"Resultado: {result}")
        return result
    except Exception as e:
        print(f"Erro no endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)

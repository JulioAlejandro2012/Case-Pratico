# Case-Pratico

## Overview

Este projeto é um sistema inteligente de processamento e classificação de e-mails corporativos, desenvolvido com FastAPI e integração com o Google Gemini AI. O sistema é capaz de:

### Funcionalidades Principais

- **Classificação Automática**: Classifica e-mails como "Produtivo" ou "Improdutivo" com base no conteúdo
- **Processamento de PDFs**: Extrai texto de arquivos PDF anexados para análise
- **Geração de Respostas**: Cria respostas automáticas profissionais e contextuais
- **Interface Web**: Frontend responsivo para upload e visualização de resultados
- **Integração com IA**: Utiliza LangChain e Google Gemini para processamento inteligente

### Arquitetura

- **Backend**: FastAPI com endpoints REST para processamento de e-mails
- **Frontend**: Interface web em HTML/CSS/JavaScript para interação do usuário
- **IA**: Modelo Gemini 2.5 Flash Lite para classificação e geração de respostas
- **NLP**: Processamento de texto e extração de conteúdo de PDFs

### Casos de Uso

- Automatização de triagem de e-mails corporativos
- Classificação de mensagens para priorização
- Geração de respostas padronizadas para e-mails comuns
- Análise de produtividade baseada no conteúdo das mensagens

## Como Configurar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Chave da API do Google Gemini
- Git

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/JulioAlejandro2012/Case-Pratico.git
   cd Case-Pratico
   ```

2. **Configure o ambiente virtual**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   No arquivo`.env` na raiz do projeto:

   ```
   GEMINI_API_KEY=sua_chave_api_aqui
   ```

   Ou configure pelo terminal:

   ```
   $env:GEMINI_API_KEY="sua_chave_api"
   ```

5. **Execute o servidor**
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```

6. **Acesse a aplicação**
   Abra seu navegador e vá para `http://localhost:8000`

### Como Usar

1. **Upload de E-mail**: Faça upload de um arquivo PDF ou TXT contendo o e-mail
2. **Inserção Manual**: Cole o texto do e-mail diretamente no campo de texto
3. **Processamento**: Clique em "Processar" para obter a classificação e resposta
4. **Resultados**: Visualize a classificação (Produtivo/Improdutivo) e a resposta gerada

### Estrutura do Projeto

```
Case-Pratico/
├── backend/
│   ├── main.py          # Servidor FastAPI principal
│   ├── agent.py         # Lógica do agente IA
│   ├── nlp.py           # Processamento de linguagem natural
│   └── rules.md         # Regras para respostas
├── frontend/
│   ├── index.html       # Interface principal
│   ├── script.js        # Lógica do frontend
│   └── style.css        # Estilos
├── requirements.txt     # Dependências Python
├── .env                # Variáveis de ambiente
└── README.md           # Este arquivo
```

### Tecnologias Utilizadas

- **FastAPI**: Framework web para o backend
- **LangChain**: Framework para integração com LLMs
- **Google Gemini AI**: Modelo de linguagem para processamento
- **PDFPlumber**: Extração de texto de PDFs
- **HTML/CSS/JavaScript**: Frontend responsivo

### Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Licença

Este projeto é para fins educacionais e de demonstração.

Desenvolvido por:
Julio Alejandro de Oliveira Montalvan
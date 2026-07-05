# QnA Assistant (Streamlit + Ollama + LangChain

A conversational AI chatbot built using **Streamlit**, **LangChain**, and **Ollama local LLMs**.  
It supports chat memory and multiple model selection with a clean ChatGPT-like UI.

---

## Features

- ChatGPT-style conversational UI
- Chat memory (remembers previous messages)
- Local LLM support using Ollama (llama3.2:1b / 3b / 7b)
- Adjustable temperature & max tokens
- Fast inference using cached model
- LangSmith tracing support (for debugging prompts)

---

## Tech Stack

- Streamlit (Frontend UI)
- LangChain (Prompt + pipeline)
- Ollama (Local LLM inference)
- Python-dotenv (Environment variables)

## How It Works

1. User enters a question
2. Chat history is stored in `st.session_state`
3. Prompt is built with previous conversation
4. Ollama LLM generates response
5. Response is stored and displayed in chat UI

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/qna-chatbot.git
cd qna-chatbot
```

### 2. Create virtual environment
- python -m venv .venv
- source .venv/bin/activate   # Mac/Linux
- .venv\Scripts\activate      # Windows

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Ollama
###### Make sure Ollama is installed and running:
```bash
ollama run llama3.2:1b
```

### 5. Run Streamlit app
```bash
python main.py # Or streamlit run app.py
```

Author

Built by Likhith

For learning Generative AI + LangChain + LLM apps

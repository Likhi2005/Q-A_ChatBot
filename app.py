import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

import os
from dotenv import load_dotenv

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []

# LangSmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_PROJECT"] = "QnA-Assistant"

# Prompt Template
template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Use chat history to answer."),
        ("user", "Previous conversation:\n{chat_history}\n\nCurrent question:\n{question}"),
    ]
)

@st.cache_resource
def load_model(llm: str):
    # Initialize the Ollama model
    # "llama3.2:1b"
    model = ChatOllama(model=llm,
            validate_model_on_init=True,)
    
    return model


def generate_response(question: str,llm,temperature,max_tokens) -> str:
    model = load_model(llm).bind(temperature=temperature, num_predict=max_tokens)
    parser = StrOutputParser()
    chat_history = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}"
        for msg in st.session_state.messages
    )
    
    chain = template | model | parser
    response = chain.invoke({"question": question,"chat_history": chat_history})
    return response

# Title of the Streamlit app
st.title("QnA Assistant with Ollama")

# Sidebar for model selection and parameters
st.sidebar.header("Model Parameters")
st.sidebar.title("Settings")

# Dropdown for selecting the model of Ollama
llm = st.sidebar.selectbox("Select Model", ["llama3.2:1b", "llama3.2:3b", "llama3.2:7b"])

# Slider for selecting the temperature of the model
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Number input for selecting the maximum tokens of the model
max_tokens = st.sidebar.number_input("Max Tokens", min_value=1, max_value=2000, value=500, step=1)

# Main Interface for user input and displaying the response
st.header("Ask a Question")
st.write("Enter your question below and click 'Get Answer' to receive a response from the Ollama model.")

# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question = st.chat_input("Ask Your Question", height=150)

if question:
    
    with st.chat_message("user"):
        st.write(question)
    
    with st.spinner("Generating response..."):
        try:
            response = generate_response(question, llm, temperature, max_tokens)
            
            # Store user message
            st.session_state.messages.append({"role": "user", "content": question})
    
            # store assistant message
            st.session_state.messages.append({"role":"assistant", "content": response})
            
            with st.chat_message("assistant"):
                st.write(response)
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
import os
import streamlit as st
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot With GROQ"

# Get API key
groq_api_key = st.secrets["GROQ_API_KEY"]

## Prompt Template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant . Please  repsonse to the user queries"),
        ("user","Question:{question}")
    ]
)

# Function to generate response
def generate_response(question, engine, temperature, max_tokens):
    llm = ChatGroq(
        model=engine,
        groq_api_key=groq_api_key,
        temperature=temperature,
        max_tokens=max_tokens
    )

    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

## #Title of the app
st.markdown("## 🤖 Sharuk's AI Assistant\n### ⚡ Powered by Groq Models")



## Sidebar for settings
st.sidebar.title("Settings")

## Select the Groq model
engine=st.sidebar.selectbox("Select Groq model",["gemma2-9b-it","llama-3.1-8b-instant","llama-3.3-70b-versatile"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=600, value=300)

## MAin interface for user input
st.write("Go ahead and ask any question")
user_input=st.text_input("You:")

if user_input:
    response = generate_response(user_input, engine, temperature, max_tokens)
    st.write(response)
else:

    st.write("Please provide a question.")

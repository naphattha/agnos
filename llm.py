import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface  import HuggingFaceEmbeddings

os.environ["LLAMA_API_KEY"] = st.secrets["LLAMA_API_KEY"]

llm = ChatGroq(
    model_name="Llama3-70B-8192",  # Make sure this model is supported
    api_key=os.getenv("LLAMA_API_KEY"),
    temperature=0.2,  # Lower temp for more factual responses
)

embeddings = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)
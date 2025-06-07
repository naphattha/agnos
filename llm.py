import os
import streamlit as st
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_groq import ChatGroq

# Set the Groq API key securely
os.environ["LLAMA_API_KEY"] = st.secrets["LLAMA_API_KEY"]

# Load LLAMA3 model from Groq
llm = ChatGroq(model="llama3-70b-8192", api_key=os.getenv("LLAMA_API_KEY"))

# HuggingFace embeddings for FAISS
embeddings = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

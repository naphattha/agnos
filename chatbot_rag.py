import os
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings  # or HuggingFaceEmbeddings

# Load vector DB created by your scraper
def load_vectorstore(path="rag_index"):
    embeddings = OpenAIEmbeddings()  # Set your API key in env
    vectorstore = FAISS.load_local(path, embeddings)
    return vectorstore

# Create RetrievalQA pipeline (RAG)
def create_qa_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    llm = ChatOpenAI(temperature=0)  # Set model + temperature
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

# Run chatbot
def chatbot_answer(question):
    qa = create_qa_chain()
    return qa.run(question)

import streamlit as st
import os
from chatbot_rag import chatbot_answer
from rag_scraper import get_documents, build_rag_index

st.set_page_config(page_title="Agnos Chatbot", page_icon="💬")

st.title("🧠 Agnos Forum Chatbot")
st.write("Ask me anything from the Agnos Health Forum!")

# Optional: Auto-update index on app start. more detail in document.
if not os.path.exists("rag_index"):
    docs = get_documents()
    build_rag_index(docs)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Your question:")
if user_input:
    with st.spinner("Thinking..."):
        st.write(f"📨 Question: {user_input}")
        response = chatbot_answer(user_input)
        st.write(f"🤖 Answer: {response}")
        st.session_state.chat_history.append((user_input, response))

for user_msg, bot_msg in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Bot:** {bot_msg}")

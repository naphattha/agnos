import streamlit as st
from chatbot_rag import chatbot_answer

st.set_page_config(page_title="Agnos Chatbot", page_icon="💬")

st.title("🧠 Agnos Forum Chatbot")
st.write("Ask me anything from the Agnos Health Forum!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Your question:")
if user_input:
    with st.spinner("Thinking..."):
        response = chatbot_answer(user_input)
        st.session_state.chat_history.append((user_input, response))

for user_msg, bot_msg in reversed(st.session_state.chat_history):
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Bot:** {bot_msg}")

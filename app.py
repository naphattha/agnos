import streamlit as st
import os
from chatbot_rag import chatbot_answer
from rag_scraper import get_documents, build_rag_index

st.set_page_config(page_title="Agnos Health Forum", page_icon="💬")

st.title("🧠 แชทบอทจากฟอรั่มสุขภาพ Agnos")
st.markdown("ถามคำถามเกี่ยวกับสุขภาพจาก [Agnos Health Forum](https://www.agnoshealth.com/forums) ได้เลย!")

# Sidebar for options
with st.sidebar:
    st.header("🔧 ตัวเลือกระบบ")
    if st.button("♻️ รีเฟรช RAG Index"):
        with st.spinner("กำลังรวบรวมข้อมูลและสร้าง Index ใหม่..."):
            docs = get_documents()
            build_rag_index(docs)
        st.success("✅ สร้าง Index ใหม่เรียบร้อยแล้ว!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input section
with st.form(key="chat_form"):
    user_input = st.text_area("🗣️ คำถามของคุณ:", placeholder="พิมพ์คำถามเกี่ยวกับสุขภาพที่นี่...", key="input_area")
    submitted = st.form_submit_button("📤 ส่งคำถาม")
    
    if submitted and user_input.strip():
        with st.spinner("🤖 กำลังคิดคำตอบ..."):
            response = chatbot_answer(user_input)
            st.session_state.chat_history.append((user_input.strip(), response))
        st.success("✅ ได้คำตอบแล้ว!")

# Display latest response
if st.session_state.chat_history:
    last_q, last_a = st.session_state.chat_history[-1]
    st.markdown("### 📨 คำถามล่าสุด")
    st.markdown(f"**{last_q}**")
    st.markdown("### 🤖 คำตอบ")
    st.markdown(last_a, unsafe_allow_html=True)

# Show full chat history
with st.expander("📚 ดูประวัติการถาม-ตอบทั้งหมด"):
    for i, (q, a) in enumerate(reversed(st.session_state.chat_history), 1):
        st.markdown(f"#### ❓ คำถาม {i}")
        st.markdown(f"**{q}**")
        st.markdown(f"**🤖 คำตอบ:**\n{a}", unsafe_allow_html=True)
        st.markdown("---")

# Footer
st.markdown("""
---
🌐 เยี่ยมชมฟอรั่มต้นฉบับ: [Agnos Health Forum](https://www.agnoshealth.com/forums)  
""")

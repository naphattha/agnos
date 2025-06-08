from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from llm import llm, embeddings  # from your llm.py

def load_vectorstore(path="rag_index"):
    print(f"📂 Loading vector store from {path}...")
    vectorstore = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    print("✅ Vector store loaded successfully.")
    return vectorstore

def create_qa_chain():
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain

def chatbot_answer(query: str) -> str:
    vectorstore = FAISS.load_local("rag_index", embeddings, allow_dangerous_deserialization=True)

    # Thai prompt template
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
คุณคือผู้ช่วยตอบคำถามเกี่ยวกับฟอรั่มสุขภาพจากเว็บไซต์ Agnos
กรุณาตอบเป็นภาษาไทยโดยอ้างอิงจากเนื้อหาต่อไปนี้:

{context}

คำถาม: {question}
คำตอบ:
""")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt_template}
    )

    result = qa_chain.run(query)
    return result.strip()
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
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

def chatbot_answer(question):
    try:
        print(f"🧠 Received question: {question}")
        qa = create_qa_chain()
        print("🔄 Running QA chain...")
        response = qa.invoke({"query": question})
        print("👉 DEBUG: Response from QA:", response)
        return response.get("result", "⚠️ No result found in response.")
    except Exception as e:
        import traceback
        print("❌ Exception in chatbot_answer")
        print("Full traceback:", traceback.format_exc())
        return f"❌ Internal error: {str(e)}"


import requests
from bs4 import BeautifulSoup
import os
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from llm import embeddings  # use HuggingFaceEmbedding from your llm.py

FORUM_URL = "https://www.agnoshealth.com/forums"
FAISS_INDEX_DIR = "rag_index"

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; AgnosScraperBot/1.0)"
}

# 1. Scrape the forum homepage for post links
def get_forum_links():
    response = requests.get(FORUM_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    post_links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/forums/" in href and href.count("/") > 2:
            full_url = "https://www.agnoshealth.com" + href
            if full_url not in post_links:
                post_links.append(full_url)

    return post_links

# 2. Scrape the content of each forum post
def scrape_post(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.title.string.strip() if soup.title else "No Title"
    
    # Generic content scraper: you might need to refine this!
    body_divs = soup.find_all("div", class_=re.compile("post|content|body"))
    body_text = "\n\n".join([div.get_text(separator=" ", strip=True) for div in body_divs])
    
    return f"{title}\n\n{body_text}"

# 3. Build documents for RAG
def get_documents():
    print("🔍 Fetching forum post links...")
    links = get_forum_links()
    print(f"✅ Found {len(links)} posts. Scraping content...")

    documents = []
    for url in links:
        try:
            content = scrape_post(url)
            documents.append(content)
        except Exception as e:
            print(f"⚠️ Failed to fetch {url}: {e}")
    return documents

# 4. Build & Save FAISS index
def build_rag_index(texts, save_path=FAISS_INDEX_DIR):
    print("📑 Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.create_documents(texts)
    print(f"🔢 Created {len(chunks)} chunks.")

    print("🧠 Creating vector store...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(save_path)
    print(f"✅ FAISS index saved at: {save_path}")

if __name__ == "__main__":
    docs = get_documents()
    print(f"📄 Scraped {len(docs)} documents. Updating RAG DB...")
    build_rag_index(docs)

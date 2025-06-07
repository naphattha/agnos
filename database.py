import requests
from bs4 import BeautifulSoup
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings  # You can swap with HuggingFace
import pickle

# === STEP 1: Scrape forum data ===

def scrape_forum(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # You may need to adjust based on actual HTML structure
    posts = soup.find_all('div', class_='topic-title')  # <-- adjust if needed
    scraped_data = []

    for post in posts:
        title = post.text.strip()
        link = post.find('a')['href']
        full_link = f"https://www.agnoshealth.com{link}"
        content = scrape_post(full_link)
        scraped_data.append({'title': title, 'url': full_link, 'content': content})
    
    return scraped_data

def scrape_post(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    post_body = soup.find('div', class_='post-body')  # adjust if needed
    if post_body:
        return post_body.text.strip()
    return ""

# === STEP 2: Process text and update FAISS ===

def create_rag_db(docs, save_path="rag_index"):
    texts = [f"{doc['title']}\n\n{doc['content']}" for doc in docs]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_texts = splitter.create_documents(texts)

    embeddings = OpenAIEmbeddings()  # Replace with your API key set in env
    vectorstore = FAISS.from_documents(split_texts, embeddings)

    vectorstore.save_local(save_path)
    print(f"RAG index saved to: {save_path}")


if __name__ == "__main__":
    forum_url = "https://www.agnoshealth.com/forums"
    print("Scraping forum...")
    data = scrape_forum(forum_url)

    print(f"Scraped {len(data)} posts. Updating RAG database...")
    create_rag_db(data)
    print("✅ Done.")

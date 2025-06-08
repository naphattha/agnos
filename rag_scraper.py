# rag_scraper.py

import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from llm import embeddings

FAISS_INDEX_DIR = "rag_index"

def init_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_documents():
    driver = init_driver()
    wait = WebDriverWait(driver, 10)
    results = []
    page = 1

    try:
        driver.get("https://www.agnoshealth.com/forums")
        time.sleep(5)

        while True:
            print(f"🔍 Scraping page {page}...")
            article_elements = driver.find_elements(By.TAG_NAME, "article")
            article_count = len(article_elements)

            for i in range(article_count):
                try:
                    article_elements = driver.find_elements(By.TAG_NAME, "article")
                    article = article_elements[i]

                    info = article.find_element(By.CSS_SELECTOR, "p.text-sm.text-gray-500").text
                    title = article.find_element(By.CSS_SELECTOR, "p.font-bold").text
                    tag_elements = article.find_elements(By.CSS_SELECTOR, "ul.flex.flex-row.gap-2 li")
                    tags = [tag.text for tag in tag_elements]
                    question_preview = article.find_element(By.CSS_SELECTOR, "div.mt-4 > p").text
                    answered = "แพทย์ตอบคำปรึกษาแล้ว" in article.text

                    # Open detail page
                    driver.execute_script("arguments[0].scrollIntoView(true);", article)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", article)
                    time.sleep(2)

                    # Extract question and answer
                    try:
                        full_question = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-gray-500"))).text
                    except:
                        full_question = None

                    try:
                        answer_el = driver.find_element(By.CSS_SELECTOR, "li.flex.flex-col.justify-between.p-4 p.mt-4")
                        doctor_name = driver.find_element(By.CSS_SELECTOR, "li.flex.flex-col.justify-between.p-4 p.font-bold").text
                        answer = answer_el.text
                    except:
                        answer = None
                        doctor_name = None

                    # Compose content for chatbot
                    content = f"""
หัวข้อ: {title}
ผู้โพสต์: {info}
แท็ก: {', '.join(tags)}
คำถามย่อ: {question_preview}
คำถามเต็ม: {full_question}
คำตอบ: {answer if answer else 'ยังไม่มีคำตอบ'}
แพทย์ผู้ตอบ: {doctor_name if doctor_name else 'ยังไม่มี'}
                    """

                    doc = Document(
                        page_content=content.strip(),
                        metadata={
                            "source": driver.current_url,
                            "title": title,
                            "tags": tags,
                            "doctor": doctor_name,
                            "answered": answered
                        }
                    )
                    results.append(doc)

                    driver.back()
                    time.sleep(2)
                except Exception as e:
                    print(f"❌ Error on article {i}: {e}")
                    continue

            # Next page
            try:
                next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'ถัดไป')]")))
                next_btn.click()
                time.sleep(3)
                page += 1
            except:
                print("✅ Reached last page.")
                break
    finally:
        driver.quit()

    return results

def build_rag_index(docs, save_path=FAISS_INDEX_DIR):
    print("📑 Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    if not chunks:
        print("⚠️ No chunks created. Aborting FAISS index creation.")
        return

    print(f"🔢 Created {len(chunks)} chunks.")
    print("🧠 Creating vector store...")

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(save_path)
    print(f"✅ FAISS index saved at: {save_path}")

# Optional main for CLI
if __name__ == "__main__":
    docs = get_documents()
    if docs:
        build_rag_index(docs)

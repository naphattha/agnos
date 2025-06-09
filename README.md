# 🧠 Agnos Health Forum Chatbot

This project implements an LLM (Large Language Model) chatbot with a RAG (Retrieval-Augmented Generation) pipeline, specifically designed to answer health-related questions by leveraging data from the [Agnos Health Forum](https://www.agnoshealth.com/forums). This chatbot aims to retrieve relevant information from the forum and provide accurate responses to user queries.

The project was developed as part of a data science assignment for Agnos, focusing on creating business value from data.

## ✨ Features

* **RAG Pipeline:** Utilizes a Retrieval-Augmented Generation (RAG) pipeline to enhance the LLM's knowledge with domain-specific information from the Agnos Health Forum.
* **Private Dataset Integration:** Integrates with a private dataset (the Agnos Health Forum) to provide contextual and accurate answers.
* **Web Scraper:** Includes a Python script (`rag_scraper.py`) that automatically scrapes data from the Agnos Health Forum to update the RAG database, fulfilling the bonus requirement.
* **Streamlit Chat Interface:** Provides a user-friendly web interface built with Streamlit for easy interaction with the chatbot, fulfilling the bonus requirement.
* **Open-source LLM & RAG:** Built using open-source technologies like LangChain for RAG and Llama3-70B for the LLM.

## 🛠️ Technologies Used

* **LLM:** Llama3-70B-8192 via Groq API
* **Embeddings:** `intfloat/multilingual-e5-base` (HuggingFace Embeddings)
* **RAG Framework:** LangChain 
* **Vector Store:** FAISS
* **Web Scraping:** Selenium, `webdriver-manager`
* **Web Interface:** Streamlit 
* **Dependencies:** Managed with `requirements.txt` 

## 🚀 Getting Started

Follow these instructions to set up and run the chatbot locally.

### Prerequisites

* Python 3.9+
* Groq API Key (for Llama3-70B)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/naphattha/LLM-chatbot-with-private-dataset.git
    cd LLM-chatbot-with-private-dataset
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    .\venv\Scripts\activate.bat
    ```
    You should then see `(venv)` at the start of your command line, indicating the virtual environment is active.

3.  **Upgrade pip and install dependencies:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt -v
    ```

4.  **Set up your Groq API Key:**
    Create a `streamlit_secrets.toml` file in a hidden folder `.streamlit` in your project root and add your Groq API key:

    `.streamlit/secrets.toml`
    ```toml
    LLAMA_API_KEY = "YOUR_GROQ_API_KEY_HERE"
    ```
    *Note: The `llm.py` file uses `st.secrets["LLAMA_API_KEY"]` to access this key.*

### Building the RAG Index

Before running the chatbot, you need to scrape the data from the Agnos Health Forum and build the FAISS RAG index.

```bash
python rag_scraper.py
```
### This script will:

* Initialize a Chrome WebDriver (headless).
* Navigate through the Agnos Health Forum pages.
* Extract relevant information (title, question, answer, tags, doctor name) from each article.
* Create LangChain Document objects.
* Split the documents into chunks.
* Create a FAISS vector store from the chunks and save it locally in the rag_index directory.
  
### Running the Chatbot
After building the RAG index, ensure your virtual environment is active, then run the Streamlit application:
```bash
python -m streamlit run app.py
```
This will open the chatbot interface in your web browser.

### Deactivating the Virtual Environment
To deactivate the virtual environment when you are done:
```Bash
deactivate
```
You can always reactivate the virtual environment later with: .\venv\Scripts\activate.bat.

### Cleaning Up
To remove the virtual environment (e.g., for a clean reinstall):
```Bash
rm -rf venv
```
(On Windows, you can also simply delete the venv folder.)

### 💡 Usage
* Refresh RAG Index: In the sidebar of the Streamlit app, you can click "♻️ รีเฟรช RAG Index" to re-scrape the forum and rebuild the RAG index.
* Ask Questions: Type your health-related questions in the input area and click "📤 ส่งคำถาม" to get answers from the chatbot.
* View History: Expand the "📚 ดูประวัติการถาม-ตอบทั้งหมด" section to see your full chat history.

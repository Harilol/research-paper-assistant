# 📄 Research Paper Assistant

> **Upload a research paper. Ask anything about it. Get precise answers — instantly.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-yellow)](https://langchain.com)
[![FAISS](https://img.shields.io/badge/VectorDB-FAISS-blueviolet)](https://faiss.ai)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?logo=streamlit)](https://streamlit.io)
[![LLM](https://img.shields.io/badge/LLM-Groq%20Llama--3.1--8b-green)](https://groq.com)

---

## 🔍 What is this?

**Research Paper Assistant** is an AI-powered chatbot that lets you upload any research paper (PDF) and have a natural conversation with it. Powered by **Retrieval-Augmented Generation (RAG)**, it doesn't just keyword-search your document — it understands context and gives you synthesized, relevant answers.

Perfect for students, researchers, and anyone who wants to extract insights from dense academic papers without reading every word.

---

## 🏗️ How It Works (RAG Pipeline)

```
        ┌─────────────────┐
        │   Upload PDF    │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Text Extraction │  ◄── PyPDF / PDFPlumber
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Text Chunking  │  ◄── Split into overlapping chunks
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │   Embeddings    │  ◄── HuggingFace / OpenAI Embeddings
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  FAISS Index    │  ◄── In-memory vector store
        └────────┬────────┘
                 │
          User asks question
                 │
                 ▼
        ┌─────────────────┐
        │ Semantic Search │  ◄── Top-k relevant chunks retrieved
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Groq LLM       │  ◄── Llama-3.1-8b synthesizes answer
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Answer in UI   │
        └─────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 **PDF Upload** | Upload any research paper directly through the UI |
| 🧠 **RAG-based Q&A** | Retrieves only the relevant chunks before answering — not the entire paper |
| ⚡ **Fast Inference** | Groq's free tier gives near-instant responses |
| 🖥️ **Clean Streamlit UI** | Simple, minimal interface — upload and start chatting |
| 🆓 **Zero Cost** | Groq free tier + free embedding models — costs nothing to run |

---

## ⚠️ Known Limitation — Embeddings Are Not Persisted

This app uses **FAISS (in-memory vector store)**. This means:

- Every time you **restart the app**, the PDF is re-processed and re-embedded from scratch
- There is **no saved index** — embeddings live only in RAM during the session
- For large papers this adds a few seconds of wait time on each restart

### 💡 Recommended Upgrade: Switch to ChromaDB

If you want **persistent embeddings** (process once, reuse forever), replace FAISS with **ChromaDB**:

```python
# Instead of FAISS:
# from langchain.vectorstores import FAISS
# vectorstore = FAISS.from_documents(docs, embeddings)

# Use ChromaDB:
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"   # saved to disk!
)
vectorstore.persist()

# Next time, just load it — no re-embedding needed:
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

ChromaDB saves the index to a local folder (`./chroma_db`). Once a paper is embedded, it never needs to be processed again — even after restarting. This is the recommended approach for production use.

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| RAG Framework | LangChain |
| LLM | Groq — `llama-3.1-8b-instant` |
| Vector Store | FAISS (in-memory) |
| Embeddings | HuggingFace Sentence Transformers |
| PDF Parsing | PyPDF |
| UI | Streamlit |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Harilol/research-paper-assistant.git
cd research-paper-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the root directory:

```bash
GROQ_API_KEY="your-groq-api-key-here"
```

Get your free Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run the app

```bash
streamlit run app.py
```

Open `http://localhost:8501`, upload a PDF, and start asking questions!

---

## 💡 Example Questions to Ask

```
"What is the main contribution of this paper?"
"Explain the methodology used in this study"
"What datasets were used for evaluation?"
"Summarize the results section"
"What are the limitations mentioned by the authors?"
```

---

## 📁 Project Structure

```
research-paper-assistant/
├── app.py              # Main Streamlit app + RAG pipeline
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
├── .gitignore
└── README.md
```

---

## 🔮 Roadmap

- [ ] Migrate from FAISS to ChromaDB for persistent embeddings
- [ ] Support multiple PDFs simultaneously
- [ ] Add chat history / memory across turns
- [ ] Highlight source chunks used for each answer
- [ ] Deploy on Streamlit Cloud

---

## 🧑‍💻 Author

**Harilol (Narasimha Reddy)**
Final-year B.Tech AI & Data Science | Aspiring AI for Drug Discovery researcher

[GitHub](https://github.com/Harilol) · [LinkedIn](https://www.linkedin.com/in/YOUR-USERNAME)

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with LangChain + FAISS + Groq + Streamlit*

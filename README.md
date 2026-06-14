# Research Paper Assistant 📄

An AI-powered chatbot that lets you upload research papers and ask questions about them.

## Features
- Upload any PDF research paper
- Ask questions in natural language
- Remembers conversation history
- Answers based only on the uploaded document

## Tech Stack
- LangChain
- LangGraph
- Groq 
- FAISS
- HuggingFace Embeddings
- Streamlit

## How to Run

1. Clone the repo
2. Install dependencies:
   pip install -r requirements.txt
3. Create a .env file and add your Groq API key:
   GROQ_API_KEY=your-key-here
4. Run the app:
   streamlit run app.py
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatGroq(model="llama-3.1-8b-instant")

def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(pages)
    return chunks

def create_vectorstore(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    texts = [doc.page_content.encode('utf-8', errors='replace').decode('utf-8') for doc in chunks]
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore

def get_chain(retriever):
    store = {}

    def get_session_history(session_id):
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]

    def get_context(input):
        docs = retriever.invoke(input["input"])
        return "\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer only from the context below.\nContext: {context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = (
        RunnablePassthrough.assign(context=get_context)
        | prompt
        | llm
        | StrOutputParser()
    )

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history"
    )


st.title("Research Paper Assistant 📄")
st.write("Upload a research paper and ask questions about it.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Processing PDF..."):
        chunks = load_pdf("temp.pdf")
        vectorstore = create_vectorstore(chunks)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        chain = get_chain(retriever)

    st.success("PDF loaded! Ask anything.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input("Ask something about the paper...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.spinner("Thinking..."):
            response = chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "session1"}}
            )

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)
# streamlit_app.py

import os
import streamlit as st
from tempfile import NamedTemporaryFile

from document_loader import (
    load_from_pdf,
    load_from_url,
    load_default_documents,
    split_documents,
)
from vector_store import store_documents
from graph_logic import web_search, retrieve, route_question, GraphState

# Set page config
st.set_page_config(page_title="Agentic RAG", layout="centered")

# Title
st.title(" Agentic RAG Demo")

# --- Sidebar Uploads ---
st.sidebar.header(" Upload Options")

user_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
user_url = st.sidebar.text_input("Or enter a URL")

# --- Load Documents ---
documents = []

if user_pdf:
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(user_pdf.read())
        tmp_file_path = tmp_file.name
    documents.extend(load_from_pdf(tmp_file_path))
    os.remove(tmp_file_path)
    st.sidebar.success(" PDF processed")

elif user_url:
    documents.extend(load_from_url(user_url))
    st.sidebar.success(" URL loaded")

else:
    documents = load_default_documents()
    st.sidebar.info("Using default URLs")

# --- Store in Vector DB ---
if documents:
    chunks = split_documents(documents)
    store_documents(chunks)
    st.sidebar.success("Documents stored in vector DB")

# --- User Input for Question ---
st.markdown("### Ask a question:")
question = st.text_input("Your question")

if st.button("Submit") and question:
    # Explicitly declare state type
    state: GraphState = {"question": question, "generation": "", "documents": []}

    route = route_question(state)
    if route == "web_search":
        state = web_search(state)
    else:
        state = retrieve(state)

    # --- Show Results ---
    st.markdown("###  Answer:")
    st.write(state["generation"])

    with st.expander(" Context Documents Used"):
        for i, doc in enumerate(state["documents"]):
            st.markdown(f"**Chunk {i+1}:**\n```\n{doc.page_content[:1000]}\n```")
else:
    st.info("Please upload a PDF, enter a URL, or use default sources and ask a question.")

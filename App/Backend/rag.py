import os
from Backend.Graph.graph import run_mediassist_graph


# Document loaders
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    CSVLoader
)

from Backend.vector_store import (
    create_embeddings,
    store_embeddings
)

# Used to split big documents into small chunks
from langchain_text_splitters import RecursiveCharacterTextSplitter


# =========================
# LOAD UPLOADED FILES
# =========================

def load_files(file_paths):
    """
    This function receives uploaded file paths.
    It reads PDF/DOCX/CSV files,
    splits text into chunks,
    creates embeddings,
    and stores them in FAISS.
    """
    total_chunks = 0

    for file_path in file_paths:
        # Get only file name from full path
        # Example: uploads/admission.pdf -> admission.pdf
        file_name = os.path.basename(file_path)

        # Get file extension
        # Example: admission.pdf -> .pdf
        ext = os.path.splitext(file_path)[1].lower()

        # Select loader based on file type
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)

        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)

        elif ext == ".csv":
            loader = CSVLoader(file_path)
        
        elif ext in [".png", ".jpg", ".jpeg"]:
            from Backend.Agents.multi_modal_agent import multi_modal_agent
            docs = multi_modal_agent.run(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

        # Read document content
        if ext in [".png",".jpg",".jpeg"]:
            pass
        else:
            docs = loader.load()

        # Split big text into small pieces
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        chunks = text_splitter.split_documents(docs)

        # Convert LangChain Document objects into plain text
        text_chunks = []

        for chunk in chunks:
            text_chunks.append(chunk.page_content)

        # If no text found, skip this file
        if len(text_chunks) == 0:
            continue

        # Convert text chunks into embeddings
        embeddings = create_embeddings(text_chunks)

        # Store embeddings with file name
        store_embeddings(
            file_name,
            text_chunks,
            embeddings
        )
        total_chunks += len(text_chunks)

    return total_chunks

# =========================
# ASK QUESTION
# =========================

def ask_question(question):
    return run_mediassist_graph(question)

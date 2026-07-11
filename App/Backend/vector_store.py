import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer


# =========================
# Paths (PERSISTENCE LAYER)
# =========================
BASE_DIR = "data"
INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")
CHUNKS_PATH = os.path.join(BASE_DIR, "chunks.pkl")
os.makedirs(BASE_DIR, exist_ok=True)

# =========================
# Load embedding model
# =========================
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dimension = 384  #embedding model produces vectors of size 384

# =========================
# load an existing FAISS vector database if available, otherwise create a new empty FAISS index.
# =========================

if os.path.exists(INDEX_PATH):
    index = faiss.read_index(INDEX_PATH) #Load saved FAISS index from disk
    print("FAISS index loaded from disk.")
else:
    index = faiss.IndexFlatL2(dimension)  #Create new FAISS index
    print("New FAISS index created.")

# =========================
# Load stored chunks : restore stored document chunks from disk when the application starts.
# =========================
if os.path.exists(CHUNKS_PATH):
    with open(CHUNKS_PATH, "rb") as f:
        document_chunks = pickle.load(f)
    print(f"Loaded {len(document_chunks)} stored chunks.")
else:
    document_chunks = []

# =========================
# Embeddings
# =========================
def create_embeddings(text_chunks):
    embeddings = embedding_model.encode(text_chunks, show_progress_bar=True)
    return np.array(embeddings).astype("float32")

# =========================
# Store embeddings + persist
# =========================
def store_embeddings(file_name, text_chunks, embeddings):
    global index, document_chunks 
    #It ensures all functions use and modify the SAME FAISS index 
    # and chunk memory instead of creating local copies.

    index.add(embeddings)  #those vectors get stored for fast similarity search.
    for chunk in text_chunks:
        document_chunks.append({"file_name":file_name, "chunk":chunk})
    #document_chunks.extend(text_chunks)
    save_data()
    #after this it will store like 
    #0 → policy.pdf | Insurance claim...
    #1 → policy.pdf | Medical reimburse..

def save_data():
    faiss.write_index(index, INDEX_PATH) ## Save FAISS index
    with open(CHUNKS_PATH, "wb") as f:   # Save chunks
        pickle.dump(document_chunks, f)



# =========================
# Search
# =========================

def search_similar_chunks(question, k=5):

    if len(document_chunks) == 0:
        return [], []

    # Convert question to embedding
    question_embedding = embedding_model.encode([question])

    # Search FAISS
    distances, indices = index.search(
        np.array(question_embedding).astype("float32"),
        k
    )

    retrieved_chunks = []
    best_index = indices[0][0]   # # Find best matching file from Rank 1 result
    if best_index == -1:
        return [], []

    best_file = document_chunks[best_index]["file_name"]

    # Return only chunks from best matching file
    for i in indices[0]:
        if i != -1 and document_chunks[i]["file_name"] == best_file:
            retrieved_chunks.append(document_chunks[i]["chunk"])
    return retrieved_chunks, [best_file]


# =========================
# Get Uploaded Files  
# =========================s
def get_uploaded_files():
    files = set() #Creates an empty set.A set automatically removes duplicates.
    for item in document_chunks:
        files.add(item["file_name"]) #Adds only filename to set.
    return sorted(list(files))  #convert set into list as JSON cannot directly use set.

# =========================
# Delete File - Deletes all vectors from FAISS and 
# recreates the index again using only the remaining files.
# =========================
def delete_file(file_name):
    global index, document_chunks
    # Remove file chunks
    #Go through all stored chunks
    #Keep only chunks whose file_name is NOT equal to the deleted file
    remaining_data = [
        item
        for item in document_chunks
        if item["file_name"] != file_name
    ]
    document_chunks = remaining_data
    # Rebuild FAISS
    index = faiss.IndexFlatL2(dimension) #creates a completely empty FAISS index.
    if len(document_chunks) > 0:
        all_chunks = [
            item["chunk"]
            for item in document_chunks
        ]
        embeddings = create_embeddings(all_chunks)
        index.add(embeddings)
    save_data()
    return f"{file_name} deleted successfully"
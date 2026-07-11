import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from Backend.rag import load_files, ask_question
#import uuid
from Backend.vector_store import (get_uploaded_files, delete_file)
import pickle


app=FastAPI()
app.add_middleware(CORSMiddleware,      #Allows frontend (Streamlit) to call backend
                   allow_origins=["*"],  #allow requests from ANY domain
                   allow_credentials=True, #Allows cookies, authentication headers, or sessions to be sent
                   allow_methods=["*"], #Allows ALL HTTP methods: Get post
                   allow_headers=["*"],)  #Allows frontend to send ANY headers Authorization, Content-Type
UPLOAD_DIR="uploads"   #all uploaded files saved here
print("APP STARTING...")

# Create uploads directory if it doesnt exist
os.makedirs(UPLOAD_DIR,exist_ok=True)


#checks backend is alive
@app.get("/")
def home():
    return{"message":"Backend running....."}

#POST API for file upload
@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)): #This API accepts multiple uploaded files asynchronously from a form request
    try:
        file_paths = []
        uploaded = []
        skipped = []

        # Save uploaded files
        for file in files:
            #unique_name = f"{uuid.uuid4()}_{file.filename}"
            #file_path = os.path.join(UPLOAD_DIR, unique_name)   #creates full path:data/abc.pdf
            #unique_name = f"{file.filename}"
            #file_path = os.path.join(UPLOAD_DIR, unique_name)
            file_path = os.path.join(UPLOAD_DIR, file.filename)  #uploads/abc.pdf

            if os.path.exists(file_path):
                skipped.append(file.filename)
                return {"error": f"{file.filename} already uploaded"} #CHECK IF FILE ALREADY EXISTS
                                
            
            with open(file_path, "wb") as f:
                f.write(await file.read())  #reads uploaded file bytes & The uploaded file is physically saved on backend machine. 
            file_paths.append(file_path) #stores path for processing
            uploaded.append(file.filename) #Storing original filename

        # Process files (chunks + embeddings + FAISS storage)
        chunks_created = load_files(file_paths)

        return {
            #"message": f"{len(files)} file(s) uploaded successfully",
            "uploaded": uploaded,
            "skipped": skipped,
            "chunks_created": chunks_created
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")  #POST endpoint for chatbot
async def ask(data:dict):    #receives JSON like { "question": "what is diabetes?" }
    try:
       question = data.get("question")  #extract question
       if not question:
            return {"error": "No question provided"}
       result=ask_question(question)
       return{
           "answer":result["answer"],
           "sources":result["sources"]}
        
    except Exception as e:
        return{
            "error":str(e)
        }



@app.get("/files")
def list_uploaded_files():
    try:
        # get full paths
        files = get_uploaded_files()
        #file_paths = glob.glob(os.path.join(UPLOAD_DIR, "*"))

        # extract only file names
        #files = [os.path.basename(f) for f in file_paths]

        return {
            "total_files": len(files),
            "files": files
        }

    except Exception as e:
        return {"error": str(e)}

@app.delete("/delete/{file_name}")
def remove_file(file_name: str):
    try:
        message = delete_file(file_name)
        # Optional: delete physical file too
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        return {
            "message": message
        }
    except Exception as e:
      return {"error": str(e)}
      


@app.get("/dashboard-data")
def dashboard_data():
    try:
        log_file = "Backend/Logs/mediassist.log"
        chunks_path = "data/chunks.pkl"

        logs = []
        document_chunks = []

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                logs = f.readlines()

        if os.path.exists(chunks_path):
            with open(chunks_path, "rb") as f:
                document_chunks = pickle.load(f)

        return {
            "logs": logs,
            "document_chunks": document_chunks
        }

    except Exception as e:
        return {"error": str(e)}

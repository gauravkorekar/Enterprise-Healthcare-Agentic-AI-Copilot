## Enterprise Healthcare Agentic AI Copilot

### Project Overview

The goal of this project is to build an AI-powered healthcare assistant
that helps hospital staff access information from multiple sources
through a single chat interface.

The system combines Retrieval-Augmented Generation (RAG), Multi-Agent
AI, Multimodal AI, MCP-based database access, and cloud deployment to
provide accurate and contextual healthcare information.

### Problem Statement

Hospitals keep information in many different places, such as SOPs,
policies, patient records, appointment systems, billing systems, and
medical reports.

Because the information is spread across multiple systems, finding the
right data can take a lot of time and effort.

The goal is to build a single AI assistant that can connect to all these
sources and provide fast, accurate, and relevant answers whenever
needed.

### Project Objectives

The system should be able to:

-   Answer questions from healthcare documents
-   Retrieve patient-related information from databases
-   Analyze uploaded medical reports and prescription images
-   Provide healthcare-related recommendations
-   Support operational and analytical queries
-   Use AI agents to perform different tasks automatically
-   Ensure responses are grounded and reliable

### Users

  User Type                  Purpose
  -------------------------- ----------------------------------------------------
  Doctor                     View patient history, reports, and recommendations
  Front Desk Staff           Check appointments and patient details
  Insurance Team             Verify insurance and billing information
  Hospital Administrator     Monitor operations and analytics
  Clinical Operations Team   Access workflows and procedures

### Data Source

| Data Source | File Format / Source | Purpose |
|-------------|----------------------|---------|
| Hospital SOPs | PDF, DOCX, TXT | Enterprise document retrieval using RAG |
| Clinical Workflow Documents | PDF, DOCX | Clinical process guidance and workflows |
| Insurance Policies | PDF, DOCX | Insurance-related queries and policy retrieval |
| Healthcare Compliance Guidelines | PDF | Regulatory and compliance information |
| Discharge Summaries | PDF | Patient discharge information retrieval |
| Operational Manuals | PDF, DOCX | Hospital operational guidance |
| Escalation Workflows | PDF | Standard escalation procedures |
| Prescriptions | PNG, JPG, JPEG | OCR and multimodal analysis |
| Medical Report Images | PNG, JPG, JPEG | Vision-based report understanding |
| Lab Report Screenshots | PNG, JPG, JPEG | Information extraction from reports |
| PostgreSQL Database | Patients, Admissions, Appointments, Doctors, Departments, Billing, Lab Results, Prescriptions, Insurance Policies, Hospital Branches | Structured data retrieval using MCP tools |

### Functional Requirements

-   Users should be able to ask healthcare-related questions through a
    chat interface.
-   Users should be able to upload PDF documents for information
    retrieval.
-   Users should be able to upload prescription and medical report
    images for analysis.
-   The system should retrieve information from enterprise documents
    using RAG.
-   The system should retrieve structured data through MCP-enabled
    PostgreSQL tools.
-   The system should generate grounded responses with citations and
    context.
-   The system should evaluate responses for relevance and hallucination
    risks.

### Requirement Understanding / Proposed Workflow

``` text
User
 │
 ▼
Streamlit UI
 │
 ▼
FastAPI Backend
 │
 ▼
LangGraph Orchestrator
 │
 ├── Planner Agent
 ├── Retriever Agent
 ├── MCP Agent
 ├── Multimodal Agent
 │
 ▼
Reasoning Agent
 │
 ▼
Evaluation Agent
 │
 ▼
Final Response
```

### Project Modules

##### 1. Data Ingestion
PDF/image ingestion, chunking, embeddings, and metadata creation.

#### 2. Enterprise RAG
Vector indexing, semantic/hybrid search, and grounded retrieval using
FAISS/ChromaDB.

#### 3. Multi-Agent System
Build agents (Planner, Retriever, MCP, Multimodal, Reasoning,
Evaluation) using LangGraph.

#### 4. MCP Server
Create MCP tools with PostgreSQL connectors and secure tool workflows.

#### 5. Multimodal AI
Enable vision-based medical image and report understanding.

#### 6. Evaluation & Observability
LLM-as-a-Judge, hallucination checks, and system monitoring.

#### 7. Guardrails
Add safety for prompt injection, data leakage, unsafe outputs, and tool
misuse.

#### 8. Dockerization
Build Docker setup with Dockerfile and Docker Compose.

#### 9. Deployment
Deploy Streamlit + FastAPI app.

### Frontend Features (Streamlit)
-   AI chatbot with streaming responses for real-time interaction.
-   PDF upload for SOPs, policies, and reports.
-   Image upload for prescriptions and lab reports.
-   Dashboard.

### Technologies Used
-   Streamlit
-   FastAPI
-   LangChain
-   LangGraph
-   OpenAI/Groq
-   FAISS/ChromaDB
-   BLIP/LLaVA
-   PostgreSQL
-   MCP
-   Docker
-   Azure

### Non-Functional Requirements

-   Modular and scalable architecture.
-   Fast response generation.
-   Secure credential management.
-   Logging, monitoring, and observability.
-   Dockerized deployment.
-   Azure cloud deployment.

### How to Run
``` bash
# Clone the repository
git clone <repository-url>
cd Enterprise-Healthcare-Agentic-AI-Copilot

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI backend
uvicorn Backend.main:app --reload

# Start the Streamlit frontend
streamlit run App/frontend/streamlit_app.py
```

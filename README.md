🧠 AI Document Assistant (Production RAG System)

📌 Project Overview

This project is a production-style AI Document Assistant that allows users to upload documents (PDF/TXT) and ask questions based on their content.

It uses a Retrieval-Augmented Generation (RAG) pipeline:

Extracts and chunks documents

Converts them into embeddings

Stores them in a FAISS vector database

Retrieves relevant context for user queries

Generates answers using a large language model

The system ensures:

✅ Accurate retrieval

✅ Source transparency

✅ Scalable architecture

⚙️ Tech Stack

Backend: FastAPI

Frontend: Streamlit

Vector DB: FAISS (with persistence)

Embeddings: Google Gemini (langchain_google_genai)

LLM: Gemini (Generative AI)

Async Processing: Celery + Redis

Language: Python

🔄 Architecture Diagram

User (Streamlit UI)

        ↓

FastAPI Backend (/upload, /query)

        ↓

Document Pipeline(PDF → Text → Clean → Chunk)

        ↓

Embedding Service (Gemini)

        ↓

FAISS Vector Store (Persistent)

        ↓

Top-K Retrieval

        ↓

Re-ranking Layer

        ↓

Context Builder

        ↓

LLM (Gemini)

        ↓

Final Answer + Sources

🚀 How to Run

1️⃣ Clone the repo

git clone https://github.com/your-username/ai-document-assistant.git

cd ai-document-assistant

2️⃣ Install dependencies

pip install -r requirements.txt

3️⃣ Set environment variables

export GOOGLE_API_KEY=your_api_key

4️⃣ Run Backend

docker-compose up

5️⃣ Run Streamlit UI

streamlit run streamlit_app.py

6️⃣ Open UI

http://localhost:8501

💡 Features

📄 Upload PDF/TXT documents

🔍 Semantic search using embeddings

🧠 Context-aware AI answers

📚 Source attribution (doc_id, chunk_id)

⚡ FAISS-based fast retrieval

💾 Persistent vector storage

🔄 Re-ranking for better accuracy

💬 Chat-based UI (Streamlit)

⚙️ Scalable architecture with Celery

📸 Screenshots

🔹 Upload Interface

<img width="418" height="525" alt="image" src="https://github.com/user-attachments/assets/8610866d-1f6f-4c50-ac25-478bad741938" />

🔹 Chat Interface

<img width="1307" height="460" alt="image" src="https://github.com/user-attachments/assets/f7b9c903-362d-401c-aace-bd58098f4fa2" />

<img width="1094" height="545" alt="image" src="https://github.com/user-attachments/assets/cafa49d1-50aa-4e34-93e4-a4ece87127ff" />

🔹 Source Attribution

<img width="1282" height="635" alt="image" src="https://github.com/user-attachments/assets/2affe3b5-e0c6-4ce7-9cac-98b1827dc38e" />

<img width="1275" height="319" alt="image" src="https://github.com/user-attachments/assets/8f38c206-10f5-436f-813e-8e01f14d6c7a" />

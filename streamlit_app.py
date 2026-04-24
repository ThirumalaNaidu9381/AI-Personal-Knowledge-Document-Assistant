import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Document Assistant", layout="wide")

st.title("📄 AI Document Assistant (RAG System)")

# -------------------------------
# Sidebar: Upload
# -------------------------------
st.sidebar.header("Upload Document")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF or TXT",
    type=["pdf", "txt"]
)

if uploaded_file is not None:
    if st.sidebar.button("Upload"):
        files = {"file": uploaded_file.getvalue()}
        
        with st.spinner("Uploading and processing..."):
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            st.sidebar.success("Upload successful ✅")
        else:
            st.sidebar.error("Upload failed ❌")

# -------------------------------
# Main: Query
# -------------------------------
st.header("Ask Questions")

query = st.text_input("Enter your question")

if st.button("Ask"):
    if not query:
        st.warning("Enter a query")
    else:
        with st.spinner("Thinking..."):
            response = requests.get(
                f"{BACKEND_URL}/query",
                params={"q": query}
            )

        if response.status_code == 200:
            data = response.json()

            st.subheader("🧠 Answer")
            st.write(data.get("answer", "No answer"))

            # -------------------------------
            # Sources (IMPORTANT for RAG)
            # -------------------------------
            st.subheader("📚 Sources")

            sources = data.get("sources", [])
            if sources:
                for i, src in enumerate(sources):
                    with st.expander(f"Source {i+1}"):
                        st.json(src)
            else:
                st.info("No sources found")

        else:
            st.error("Query failed ❌")

# -------------------------------
# Debug Section (DON’T SKIP THIS)
# -------------------------------
st.divider()
st.subheader("⚙️ Debug Info")

if st.checkbox("Show backend health"):
    try:
        r = requests.get(f"{BACKEND_URL}/docs")
        st.success("Backend is running ✅")
    except:
        st.error("Backend not reachable ❌")
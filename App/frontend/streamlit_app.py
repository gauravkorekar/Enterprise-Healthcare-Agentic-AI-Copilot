import os
import requests
import streamlit as st
from urllib.parse import quote
from dashboard import show_dashboard

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="MediAssist AI",
    page_icon="🧠",
    layout="wide"
)

st.success("✅ MediAssist frontend loaded")

page = st.sidebar.radio(
    "Navigation",
    ["💬 Chat", "📁 Upload Documents", "📊 Dashboard"]
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if page == "📊 Dashboard":
    show_dashboard()
    st.stop()

st.markdown(
    """
    <h1 style='text-align:center; color:#2E7D32;'>🏥 MediAssist AI</h1>
    <p style='text-align:center; color:gray;'>Enterprise Healthcare Copilot</p>
    """,
    unsafe_allow_html=True
)

st.divider()

if page == "📁 Upload Documents":
    st.subheader("📁 Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload Your Files",
        type=["pdf", "docx", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if st.button("Upload"):
        if not uploaded_files:
            st.warning("Please select at least one file.")
        else:
            files = [
                ("files", (f.name, f.getvalue(), "application/octet-stream"))
                for f in uploaded_files
            ]

            try:
                with st.spinner("Processing documents... ⏳"):
                    response = requests.post(
                        f"{BACKEND_URL}/upload",
                        files=files,
                        timeout=120
                    )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])
                else:
                    st.success("Documents uploaded successfully ✅")
                    st.info(f"Total chunks created: {data.get('chunks_created', 0)}")

            except Exception as e:
                st.error(f"Upload failed: {e}")

    st.divider()
    st.subheader("📂 Uploaded Files")

    try:
        res = requests.get(f"{BACKEND_URL}/files", timeout=30)
        data = res.json()

        if "error" in data:
            st.error(data["error"])
        elif data.get("files"):
            st.caption(f"Total Files: {len(data['files'])}")

            for file_name in data["files"]:
                col1, col2 = st.columns([8, 1])

                with col1:
                    st.write(f"📄 {file_name}")

                with col2:
                    if st.button("❌", key=f"delete_{file_name}"):
                        delete_res = requests.delete(
                            f"{BACKEND_URL}/delete/{quote(file_name)}",
                            timeout=30
                        )
                        delete_data = delete_res.json()

                        if "error" in delete_data:
                            st.error(delete_data["error"])
                        else:
                            st.success(delete_data["message"])

                        st.rerun()
        else:
            st.info("No documents uploaded yet.")

    except Exception as e:
        st.error(f"Unable to fetch files: {e}")

    st.stop()

if page == "💬 Chat":
    st.subheader("💬 Ask a Question")

    question = st.text_input("Type your question here:")

    if st.button("Submit"):
        if question.strip() == "":
            st.warning("Please enter a question")
        else:
            try:
                with st.spinner("Thinking... 🤖"):
                    response = requests.post(
                        f"{BACKEND_URL}/ask",
                        json={"question": question},
                        timeout=120
                    )

                data = response.json()

                if "answer" in data:
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": data["answer"],
                        "sources": data.get("sources", [])
                    })

                    st.markdown("### Answer")
                    st.markdown(data["answer"])

                    if data.get("sources"):
                        st.markdown("### 📚 Sources")
                        for source in data["sources"]:
                            st.write(f"📄 {source}")
                else:
                    st.error(data.get("error", "Unknown error occurred"))

            except Exception as e:
                st.error(f"Request failed: {e}")

    st.divider()
    st.subheader("📜 Chat History")

    with st.container(border=True, height=300):
        for chat in reversed(st.session_state.chat_history[-5:]):
            st.markdown(f"**🧑 Question:** {chat['question']}")
            st.markdown(f"**🤖 Answer:** {chat['answer']}")

            if chat.get("sources"):
                st.markdown("**📚 Sources:**")
                for source in chat["sources"]:
                    st.write(f"📄 {source}")

            st.divider()

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

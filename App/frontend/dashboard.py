import os
import re
import pandas as pd
import streamlit as st
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


def fetch_dashboard_data():
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard-data", timeout=30)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def extract_log_stats(logs):
    stats = {
        "total_questions": 0,
        "rag_queries": 0,
        "mcp_queries": 0,
        "blocked_queries": 0,
        "evaluation_count": 0,
        "avg_scores": []
    }

    for line in logs:
        if "[GRAPH] New Question" in line:
            stats["total_questions"] += 1
        if "Planner Route : rag" in line:
            stats["rag_queries"] += 1
        if "Planner Route : mcp" in line:
            stats["mcp_queries"] += 1
        if "Question blocked" in line:
            stats["blocked_queries"] += 1
        if "Average Score" in line:
            stats["evaluation_count"] += 1
            match = re.search(r"Average Score\s*:\s*([0-9.]+)", line)
            if match:
                stats["avg_scores"].append(float(match.group(1)))

    return stats


def extract_token_usage(logs):
    prompt_tokens = 0
    completion_tokens = 0
    total_tokens = 0

    for line in logs:
        if "[TOKENS]" in line:
            match = re.search(r"Prompt=(\d+).*Completion=(\d+).*Total=(\d+)", line)
            if match:
                prompt_tokens += int(match.group(1))
                completion_tokens += int(match.group(2))
                total_tokens += int(match.group(3))

    return prompt_tokens, completion_tokens, total_tokens


def show_dashboard():
    st.title("📊 MediAssist AI Dashboard")

    if st.button("🔄 Refresh"):
        st.rerun()

    data = fetch_dashboard_data()

    if "error" in data:
        st.error(f"Unable to load dashboard data: {data['error']}")
        return

    logs = data.get("logs", [])
    document_chunks = data.get("document_chunks", [])

    stats = extract_log_stats(logs)
    prompt_tokens, completion_tokens, total_tokens = extract_token_usage(logs)

    uploaded_files = sorted({
        item.get("file_name", item.get("source", "Unknown"))
        for item in document_chunks
    })

    avg_eval_score = (
        round(sum(stats["avg_scores"]) / len(stats["avg_scores"]), 2)
        if stats["avg_scores"]
        else 0
    )

    st.subheader("📌 Overview")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Uploaded Files", len(uploaded_files))
    c2.metric("Stored Chunks", len(document_chunks))
    c3.metric("Total Questions", stats["total_questions"])
    c4.metric("Average Eval Score", avg_eval_score)
    c5.metric("Total Tokens", f"{total_tokens:,}")

    st.divider()

    st.subheader("🪙 Token Usage")
    t1, t2, t3 = st.columns(3)
    t1.metric("Prompt Tokens", f"{prompt_tokens:,}")
    t2.metric("Completion Tokens", f"{completion_tokens:,}")
    t3.metric("Total Tokens", f"{total_tokens:,}")

    st.divider()

    st.subheader("🧠 Query Route Analytics")
    route_df = pd.DataFrame({
        "Route": ["RAG", "MCP", "Blocked"],
        "Count": [stats["rag_queries"], stats["mcp_queries"], stats["blocked_queries"]]
    })
    st.dataframe(route_df, width="stretch")

    st.divider()

    st.subheader("📄 Uploaded Documents")
    if uploaded_files:
        file_data = []
        for file in uploaded_files:
            chunk_count = sum(
                1 for item in document_chunks
                if item.get("file_name", item.get("source", "Unknown")) == file
            )
            file_data.append({"File Name": file, "Chunks": chunk_count})

        st.dataframe(pd.DataFrame(file_data), width="stretch")
    else:
        st.info("No uploaded documents found.")

    st.divider()

    st.subheader("🧾 Recent Logs")
    if logs:
        st.code("".join(logs[-20:]), language="text")
    else:
        st.info("No logs found.")

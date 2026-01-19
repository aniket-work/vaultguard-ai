import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from ingest import VaultGuardIngestor
from hybrid_search import HybridRetriever
from brain import LocalBrain

st.set_page_config(page_title="VaultGuard-AI Dashboard", layout="wide")

st.title("🛡️ VaultGuard-AI: Portfolio Intelligence")
st.markdown("---")

# Sidebar
st.sidebar.header("Configuration")
model_name = st.sidebar.selectbox("Local Model", ["llama3", "mistral", "phi3"])
top_k = st.sidebar.slider("Top K Results", 1, 10, 5)

# Initialize
@st.cache_resource
def get_engine():
    ingestor = VaultGuardIngestor()
    vector_db, bm25, chunks = ingestor.process_and_index()
    return HybridRetriever(vector_db, bm25, chunks), LocalBrain(model=model_name)

retriever, brain = get_engine()

# Main UI
col1, col2 = st.columns([2, 1])

with col1:
    query = st.text_input("Enter your confidential query:", "What is the expected IRR for Project X?")
    if st.button("Analyze"):
        with st.spinner("Analyzing portfolio data..."):
            context_docs = retriever.search(query, top_k=top_k)
            context = "\n".join(context_docs)
            answer = brain.ask(query, context)
            
            st.subheader("Analysis Result")
            st.write(answer)
            
            st.subheader("Retrieved Context Chunks")
            for i, doc in enumerate(context_docs):
                st.info(f"Chunk {i+1}: {doc[:200]}...")

with col2:
    st.subheader("Portfolio Health Snapshot")
    # Dummy stats for the UI component of the GIF
    data = {
        "Metric": ["Alpha", "Beta", "Sharpe", "Volatility"],
        "Value": [0.15, 1.2, 2.1, 0.08]
    }
    df = pd.DataFrame(data)
    
    fig, ax = plt.subplots()
    sns.barplot(x="Metric", y="Value", data=df, ax=ax, palette="viridis")
    st.pyplot(fig)
    
    st.table(df)

st.markdown("---")
st.caption("Experimental PoC - VaultGuard-AI Runs Locally and Securely.")

---
title: "VaultGuard-AI: Building a Local-First Hybrid Search RAG for Private Equity Intelligence"
subtitle: "How I Built a Privacy-Preserving AI Agent to Securely Analyze Confidential Portfolio Performance Locally"
tags: ["ai", "python", "rag", "privacy"]
published: true
---

![Title](https://raw.githubusercontent.com/aniket-work/vaultguard-ai/main/images/title-animation.gif)

> **How I Built a Privacy-Preserving AI Agent to Securely Analyze Confidential Portfolio Performance Locally**

# TL;DR
In my experiments with local-first AI, I observed that the greatest barrier to AI adoption in private equity is data privacy. I built VaultGuard-AI, a PoC that uses Hybrid Search (BM25 + Semantic) and Ollama to run high-fidelity RAG entirely on a local CPU. This project demonstrates how sensitive PPMs and financial reports can be analyzed without cloud exposure, achieving zero-data-leakage while maintaining professional analytical accuracy.

# Introduction
In my opinion, the "cloud-first" approach to Generative AI is fundamentally at odds with industries that thrive on confidentiality—like Private Equity and High-Net-Worth Wealth Management. From my experience, analysts often find themselves in a catch-22: they need the synthesis power of LLMs to parse 200-page Private Placement Memorandums (PPMs), but they cannot risk uploading those documents to a public API. 

I wrote this PoC because I thought there had to be a way to bridge this gap. I put it this way because the technology has finally matured to a point where a humble workstation can act as a high-security "Vault" for intelligence. As per my experiments, combining the keyword precision of BM25 with the conceptual nuances of semantic search creates a hybrid system that is more reliable than either alone, especially when dealing with dense financial jargon.

# What's This Article About?
This article details my personal journey in architecting a local-first, privacy-preserving intelligence agent. I will walk you through:
1.  The design of a **Hybrid Search Engine** that doesn't rely on cloud vector databases.
2.  How I implemented **Reciprocal Rank Fusion (RRF)** to combine sparse and dense retrieval.
3.  The integration with **Ollama** for secure, local inference.
4.  A Streamlit-based **Analytical Dashboard** for visualizing portfolio health.

As per me, this is the most practical use case for RAG in the real world today.

# Tech Stack
I chose this specific stack because it prioritizes reproducibility and local sovereignty:
- **Language**: Python 3.10 (The lingua franca for these experiments).
- **Orchestration**: LangChain (To glue the components together).
- **Vector Store**: ChromaDB (Running in-memory/on-disk locally).
- **Hybrid Search**: Rank-BM25 (For that "exact match" keyword reliability).
- **Embeddings**: `all-MiniLM-L6-v2` (Fast, CPU-friendly semantic encoding).
- **Inference**: Ollama (Specifically `llama3` for its reasoning capabilities).
- **Visualization**: Streamlit & Seaborn (For the professional UI).

# Why Read It?
If you have ever felt hesitant about pasting sensitive business data into a ChatGPT prompt, this is for you. In my experience, understanding the mechanics of local RAG is becoming a survival skill for developers working in regulated industries. I think you will find the "Hybrid" approach particularly enlightening—it solves the common "hallucination" problems that happen when semantic search misses specific financial metrics like "IRR" or "EBITDA."

# Let's Design
Before I wrote a single line of code, I had to map out the flow. I wanted a system where the document never leaves the analyst's machine.

![Architecture](https://raw.githubusercontent.com/aniket-work/vaultguard-ai/main/images/architecture-diagram.png)

From my experience, the data flow must be unidirectional. The document is chunked, indexed twice, and then retrieved based on a unified score. I think this "Dual Indexing" is the secret sauce.

# Let’s Get Cooking

### 1. The Ingestion Engine
I wrote this module to handle the "boring but critical" task of document processing. I used a recursive splitter because financial reports have hierarchical headers that shouldn't be separated from their content.

```python
# ingest.py
def process_and_index(self):
    docs = self.load_documents()
    chunks = self.text_splitter.split_documents(docs)
    
    # Dual Indexing: BM25 for keywords, Chroma for semantics
    texts = [chunk.page_content for chunk in chunks]
    tokenized_corpus = [doc.split(" ") for doc in texts]
    bm25 = BM25Okapi(tokenized_corpus)
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=self.embeddings,
        persist_directory=self.persist_dir
    )
    return vector_db, bm25, chunks
```

I put it this way because initializing both indices simultaneously ensures that our retrieval layer has two "eyes" on the data: one for words, one for meanings.

### 2. The Hybrid Search Controller
This is where I implemented Reciprocal Rank Fusion (RRF). In my opinion, RRF is the most elegant way to solve the "comparing apples to oranges" problem between vector distance and BM25 scores.

```python
# hybrid_search.py
def search(self, query, top_k=5):
    # 1. Semantic Search
    semantic_docs = self.vector_db.similarity_search(query, k=top_k*2)
    semantic_ids = [doc.page_content for doc in semantic_docs]
    
    # 2. Keyword Search (BM25)
    tokenized_query = query.split(" ")
    bm25_docs = self.bm25.get_top_n(tokenized_query, [c.page_content for c in self.chunks], n=top_k*2)
    
    # 3. Combine using RRF
    combined = reciprocal_rank_fusion([semantic_ids, bm25_docs])
    return [res[0] for res in combined[:top_k]]
```

I observed that this logic significantly reduces the "lost in the middle" problem. Even if the vector model is unsure, the BM25 component often catches the specific entity or metric name.

### 3. The Local Brain
Integration with Ollama was the final piece. I designed the prompt to be extremely restrictive—telling the agent to *only* use the provided context.

```python
# brain.py
def ask(self, query, context):
    prompt = f"Context: {context}\\nQuery: {query}\\nAnswer based ONLY on context..."
    payload = {"model": "llama3", "prompt": prompt, "stream": False}
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    return response.json().get("response")
```

I think this strictness is what makes the agent "professional" rather than "conversational."

# Let's Setup
Step by step details can be found at: [VaultGuard-AI GitHub Repo](https://github.com/aniket-work/vaultguard-ai)

1.  Initialize your environment: `python -m venv venv`
2.  Install the dependencies: `pip install -r requirements.txt`
3.  Ensure Ollama is running: `ollama run llama3`
4.  Run the engine: `python main.py`

# Let's Run
When I first ran this, I was impressed by the speed of the hybrid retrieval. The terminal output provides a technical audit trail of every step.

![Sequence](https://raw.githubusercontent.com/aniket-work/vaultguard-ai/main/images/sequence-diagram.png)

As per my experiments, the latency on a modern Mac is negligible, typically under 5 seconds for a full retrieval-plus-inference cycle.

# Closing Thoughts
My personal takeaway from building VaultGuard-AI is that we don't need million-dollar cloud contracts to build sophisticated AI assistants. I think the future of enterprise AI is local, hybrid, and open-source. This PoC proves that a private equity analyst can have a world-class researcher on their desk that never talks to the internet.

Disclaimer

The views and opinions expressed here are solely my own and do not represent the views, positions, or opinions of my employer or any organization I am affiliated with. The content is based on my personal experience and experimentation and may be incomplete or incorrect. Any errors or misinterpretations are unintentional, and I apologize in advance if any statements are misunderstood or misrepresented.

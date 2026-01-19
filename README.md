# 🛡️ VaultGuard-AI: Local-First Confidential Portfolio Intelligence

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/aniket-work/vaultguard-ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

![Title Animation](https://raw.githubusercontent.com/aniket-work/vaultguard-ai/main/images/title-animation.gif)

## 📖 Overview

**VaultGuard-AI** is a high-performance, privacy-preserving intelligence agent designed for Private Equity analysts and Wealth Managers. It enables local analysis of sensitive Private Placement Memorandums (PPMs), financial audits, and confidential reports without ever sending data to the cloud.

Built with a **Hybrid Search RAG Architecture**, it combines dense semantic retrieval with sparse keyword matching to ensure maximum accuracy for specific financial terminology and broad conceptual queries.

## 🚀 Key Features

- **100% Local Execution**: Runs entirely on your machine using Ollama and local embedding models.
- **Hybrid Search Engine**: Integrated BM25 + Semantic Vector Search with Reciprocal Rank Fusion (RRF).
- **Intelligent Chunking**: Document processing optimized for complex financial tables and reports.
- **Analytical Dashboard**: Professional Streamlit UI for deep-dive portfolio analysis and statistical visualization.
- **Technical ASCII Output**: High-fidelity terminal logs for debugging and transparency.

## 🏗️ Architecture

![System Architecture](https://raw.githubusercontent.com/aniket-work/vaultguard-ai/main/images/architecture-diagram.png)

## 🛠️ Tech Stack

- **Core**: Python 3.10+
- **Retrieval**: LangChain, ChromaDB (Vector Store), Rank-BM25 (Keyword Search)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Inference**: Ollama (Llama 3 / Mistral)
- **UI**: Streamlit, Matplotlib, Seaborn

## 🚦 Getting Started

### Prerequisites

1. Install [Ollama](https://ollama.com/).
2. Pull the required model:
   ```bash
   ollama pull llama3
   ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aniket-work/vaultguard-ai.git
   cd vaultguard-ai
   ```

2. Setup virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Engine

- **Terminal Mode (CLI)**:
  ```bash
  python main.py
  ```

- **Dashboard Mode (UI)**:
  ```bash
  streamlit run app.py
  ```

## 📊 Process Flow

![Sequence Diagram](https://raw.githubusercontent.com/aniket-work/vaultguard-ai/main/images/sequence-diagram.png)

## 📜 Disclaimer

This is an experimental proof-of-concept (PoC) project. It is intended for educational and demonstration purposes only and should not be used for production investment decisions without further auditing.

---
Developed as a personal experiment in local-first AI architectures.

import os
import streamlit as st
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from rank_bm25 import BM25Okapi
import nltk
import json
import pandas as pd

# Download necessary NLTK data
nltk.download('punkt', quiet=True)

class VaultGuardIngestor:
    def __init__(self, data_dir="data", persist_dir="vector_db"):
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def load_documents(self):
        documents = []
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            # Create a dummy file for PoC if empty
            with open(os.path.join(self.data_dir, "sample_report.txt"), "w") as f:
                f.write("VaultGuard-AI confidential investment report. Private Placement Memorandum for Project X. The expected IRR is 25%. Target geography is Southeast Asia. Risk factors include local currency volatility.")
        
        for file in os.listdir(self.data_dir):
            path = os.path.join(self.data_dir, file)
            if file.endswith(".txt"):
                loader = TextLoader(path)
                documents.extend(loader.load())
            elif file.endswith(".pdf"):
                loader = PyPDFLoader(path)
                documents.extend(loader.load())
        return documents

    def process_and_index(self):
        docs = self.load_documents()
        chunks = self.text_splitter.split_documents(docs)
        
        # Initialize Keyword Search (BM25)
        texts = [chunk.page_content for chunk in chunks]
        tokenized_corpus = [doc.split(" ") for doc in texts]
        bm25 = BM25Okapi(tokenized_corpus)
        
        # Initialize Vector Search (Semantic)
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        
        return vector_db, bm25, chunks

if __name__ == "__main__":
    ingestor = VaultGuardIngestor()
    print("Indexing documents...")
    vector_db, bm25, chunks = ingestor.process_and_index()
    print(f"Successfully indexed {len(chunks)} chunks.")

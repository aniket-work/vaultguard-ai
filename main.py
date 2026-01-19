import os
import time
from ingest import VaultGuardIngestor
from hybrid_search import HybridRetriever
from brain import LocalBrain

def main():
    print("="*60)
    print("   VAULTGUARD-AI: CONFIDENTIAL PORTFOLIO INTELLIGENCE")
    print("="*60)
    
    # 1. Ingestion
    print("\n[$] Initializing VaultGuard Engine...")
    ingestor = VaultGuardIngestor()
    vector_db, bm25, chunks = ingestor.process_and_index()
    time.sleep(1)
    
    # 2. Setup Retriever & Brain
    retriever = HybridRetriever(vector_db, bm25, chunks)
    brain = LocalBrain()
    
    # 3. Interactive Loop (Simulated for terminal GIF)
    queries = [
        "What is the expected IRR for Project X?",
        "Identify key risk factors in Southeast Asia."
    ]
    
    for query in queries:
        print(f"\n[QUERY] > {query}")
        print("[$] Searching Hybrid Knowledge Base...")
        time.sleep(0.5)
        
        context_docs = retriever.search(query)
        context = "\n".join(context_docs)
        
        print("[$] Thinking...")
        answer = brain.ask(query, context)
        
        print(f"\n[ANSWER]\n{answer}")
        print("-" * 40)
        time.sleep(1)

    print("\n[SUCCESS] VaultGuard-AI session completed.")

if __name__ == "__main__":
    main()

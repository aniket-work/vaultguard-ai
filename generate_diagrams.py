import base64
import requests
import os
import time

def generate_diagram(name, code):
    print(f"Generating {name}...")
    encoded = base64.b64encode(code.encode()).decode()
    url = f"https://mermaid.ink/img/{encoded}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with open(f"images/{name}.png", 'wb') as f:
                    f.write(response.content)
                print(f"Successfully generated images/{name}.png")
                return True
            else:
                print(f"Error {response.status_code} for {name}")
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {name}: {str(e)}")
        time.sleep(2)
    return False

diagrams = {
    "architecture-diagram": """
graph TB
    subgraph Local_Environment ["Local Workstation (Secure)"]
        A[Sensitive Docs: PDF/TXT] --> B(VaultGuard Ingestor)
        B --> C[(ChromaDB: Semantic)]
        B --> D[(BM25: Keyword)]
        E[User Query] --> F(Hybrid Retriever)
        C --> F
        D --> F
        F --> G{RRF Re-ranking}
        G --> H[Local Context]
        H --> I(Local LLM: Ollama)
        I --> J[Professional Investment Analysis]
    end
    style Local_Environment fill:#f9f9f9,stroke:#333,stroke-width:2px
    """,
    "sequence-diagram": """
sequenceDiagram
    participant Analyst
    participant Retriever
    participant VectorDB
    participant LocalLLM
    
    Analyst->>Retriever: Confidential Query
    par Semantic Search
        Retriever->>VectorDB: Similarity Query
        VectorDB-->>Retriever: Top K Dense Results
    and Keyword Search
        Retriever->>Retriever: BM25 Scoring
        Retriever-->>Retriever: Top K Sparse Results
    end
    Retriever->>Retriever: Reciprocal Rank Fusion
    Retriever->>LocalLLM: Prompt with Local Context
    LocalLLM-->>Analyst: Private Execution Result
    """,
    "flow-diagram": """
flowchart TD
    Start([Start Analysis]) --> Load[Load Private Documents]
    Load --> Split[Recursive Semantic Chunking]
    Split --> Index[Dual Indexing: Vector + Keyword]
    Index --> Query[Analyst Input Query]
    Query --> Hybrid[Hybrid Search Logic]
    Hybrid --> RRF[RRF Re-ranking]
    RRF --> Context[Augment Prompt with Local Context]
    Context --> Inference[Ollama Local Inference]
    Inference --> End([Generate Professional Report])
    """,
    "title-diagram": """
graph LR
    A[VaultGuard-AI] --- B((Local RAG))
    B --- C{Hybrid Search}
    C --- D[Confidential Intelligence]
    style A fill:#1e3a8a,color:#fff
    style D fill:#16a34a,color:#fff
    """
}

if __name__ == "__main__":
    if not os.path.exists("images"):
        os.makedirs("images")
    
    all_success = True
    for name, code in diagrams.items():
        if not generate_diagram(name, code):
            all_success = False
    
    if all_success:
        print("\nAll technical diagrams generated successfully.")
    else:
        print("\nSome diagrams failed to generate.")
        exit(1)

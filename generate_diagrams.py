import base64
import requests
import os

def generate_mermaid_diagrams():
    diagrams = {
        "title_diagram": """
graph TD
    classDef main fill:#1e1e2e,stroke:#00ffcc,stroke-width:2px,color:#fff
    classDef sub fill:#313244,stroke:#89b4fa,stroke-width:1px,color:#fff
    
    A["TalentArch-AI Platform"]:::main --> B["Deep Query Parsing"]:::sub
    B --> C["Hybrid Retrieval Engine"]:::main
    C --> D["Vector Semantic Search"]:::sub
    C --> E{"Keyword Match (BM25)"}:::sub
    D --> F["Rerank & Score Fusion"]:::main
    E --> F
    F --> G["Architectural Fit Report"]:::sub
        """,
        "architecture_diagram": """
graph LR
    User([Talent Partner]) -- "Query (Role Specs)" --> Agent[TalentArch Agent]
    subgraph Engine [Hybrid RAG Engine]
        direction TB
        BM25[BM25 Index]
        Vector[Vector DB / Embeddings]
        Fusion[Weighted Score Fusion]
    end
    Agent --> Engine
    Engine --> Data[(Resume JSON/PDF)]
    Fusion --> Rerank[Reranking Module]
    Rerank --> Output[Final Candidate Rankings]
        """,
        "sequence_diagram": """
sequenceDiagram
    participant U as User
    participant A as TalentArch Agent
    participant K as Keyword Index
    participant S as Semantic Store
    participant F as Score Fusion
    
    U->>A: Submit 'Cloud Engineer' search
    par Concurrent Retrieval
        A->>K: BM25 Keyword Search
        A->>S: Cosine Similarity Search
    end
    K-->>F: Raw Keyword Scores
    S-->>F: Semantic Match Scores
    F->>F: Weighted RRF / Linear Merge
    F-->>A: Rank Candidate List
    A-->>U: Present Final Matching Report
        """,
        "flow_diagram": """
flowchart TD
    Start([Start Search]) --> Parse[Role Requirement Extraction]
    Parse --> Search{Hybrid Retrieval}
    Search --> Vector[Semantic Vector Path]
    Search --> Keyword[BM25 Keyword Path]
    Vector --> Score[Raw Scoring]
    Keyword --> Score
    Score --> Weight[Apply Hybrid Weights]
    Weight --> Rerank[Contextual Reranking]
    Rerank --> End([Generate PDF/Console Report])
        """
    }

    img_dir = os.path.join(os.path.dirname(__file__), "images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    for name, code in diagrams.items():
        encoded = base64.b64encode(code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded}"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with open(os.path.join(img_dir, f"{name.replace('_', '-')}.png"), 'wb') as f:
                    f.write(response.content)
                print(f"[v] Generated {name}")
            else:
                print(f"[x] Failed to generate {name}: {response.status_code}")
        except Exception as e:
            print(f"[!] Error generating {name}: {e}")

if __name__ == "__main__":
    generate_mermaid_diagrams()

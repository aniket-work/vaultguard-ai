import numpy as np
from langchain_community.vectorstores import Chroma
from rank_bm25 import BM25Okapi

def reciprocal_rank_fusion(results_list, k=60):
    """
    Reciprocal Rank Fusion from 'Using Reciprocal Rank to Combine Binary Classifiers'
    """
    fused_scores = {}
    for results in results_list:
        for rank, doc_id in enumerate(results):
            if doc_id not in fused_scores:
                fused_scores[doc_id] = 0
            fused_scores[doc_id] += 1 / (rank + k)
    
    reranked_results = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    return reranked_results

class HybridRetriever:
    def __init__(self, vector_db, bm25, chunks):
        self.vector_db = vector_db
        self.bm25 = bm25
        self.chunks = chunks

    def search(self, query, top_k=5):
        # 1. Semantic Search
        semantic_docs = self.vector_db.similarity_search(query, k=top_k*2)
        semantic_ids = [doc.page_content for doc in semantic_docs]
        
        # 2. Keyword Search (BM25)
        tokenized_query = query.split(" ")
        bm25_docs = self.bm25.get_top_n(tokenized_query, [c.page_content for c in self.chunks], n=top_k*2)
        
        # 3. Combine using RRF
        combined = reciprocal_rank_fusion([semantic_ids, bm25_docs])
        
        # Return top N content
        return [res[0] for res in combined[:top_k]]

if __name__ == "__main__":
    # Test stub
    pass

import json
import os
import numpy as np
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
import time

class TalentArchAI:
    """
    Experimental Hybrid-Search RAG Agent for Skill-First Recruitment.
    Combines Keyword (BM25) and Semantic scoring (Simulated Vector Search).
    """
    def __init__(self, data_path: str):
        with open(data_path, 'r') as f:
            self.candidates = json.load(f)
        
        # Initialize BM25 for keyword search
        self.corpus = [
            " ".join(c['skills'] + [c['role'], c['summary']])
            for c in self.candidates
        ]
        tokenized_corpus = [doc.lower().split() for doc in self.corpus]
        self.bm25 = BM25Okapi(tokenized_corpus)
        
    def _simulated_vector_score(self, query: str, candidate: Dict) -> float:
        """
        Simulates a semantic vector similarity score.
        In a production PoC, this would use OpenAI/Anthropic embeddings.
        """
        # Simple overlap-based simulation for the experiment
        query_words = set(query.lower().split())
        candidate_text = " ".join([candidate['role'], candidate['summary']]).lower()
        overlap = sum(1 for word in query_words if word in candidate_text)
        return min(1.0, overlap / max(len(query_words), 1) + 0.2) # Base score + context match

    def hybrid_search(self, query: str, top_k: int = 3, semantic_weight: float = 0.6) -> List[Dict]:
        """
        Performs hybrid search by merging BM25 and semantic scores.
        """
        print(f"[*] Initializing Hybrid Search for query: '{query}'")
        time.sleep(0.5)
        
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        # Normalize BM25 scores
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
        normalized_bm25 = [s / max_bm25 for s in bm25_scores]

        results = []
        for i, candidate in enumerate(self.candidates):
            sem_score = self._simulated_vector_score(query, candidate)
            # Reciprocal Rank Fusion or Weighted Merge
            hybrid_score = (semantic_weight * sem_score) + ((1 - semantic_weight) * normalized_bm25[i])
            
            results.append({
                "candidate": candidate,
                "score": round(hybrid_score, 4),
                "keyword_score": round(normalized_bm25[i], 4),
                "semantic_score": round(sem_score, 4)
            })

        # Sort by hybrid score
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        return results[:top_k]

    def generate_report(self, query: str, top_candidates: List[Dict]):
        """
        Generates a terminal-style ASCII report for the process.
        """
        print("\n" + "="*80)
        print(f" TALENT-ARCH AI: ARCHITECTURAL TALENT MATCHING REPORT")
        print(f" TARGET PROFILE: {query}")
        print("="*80)
        print(f"{'CANDIDATE NAME':<25} | {'ROLE':<25} | {'HYBRID SCORE':<12}")
        print("-" * 80)
        
        for res in top_candidates:
            c = res['candidate']
            print(f"{c['name']:<25} | {c['role']:<25} | {res['score']:<12}")
        
        print("="*80)
        print("[+] Processing complete. Statistical visualizations available in /images")

if __name__ == "__main__":
    # Path to data
    data_file = os.path.join(os.path.dirname(__file__), "data", "mock_resumes.json")
    
    # Run Experiment
    arch = TalentArchAI(data_file)
    
    test_query = "Cloud native engineer with deep Python knowledge and CI/CD experience"
    matches = arch.hybrid_search(test_query)
    arch.generate_report(test_query, matches)

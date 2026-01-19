import requests
import json

class LocalBrain:
    def __init__(self, model="llama3"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def ask(self, query, context):
        prompt = f"""
        You are VaultGuard-AI, a professional Private Equity Intelligence Agent.
        Use ONLY the following context to answer the user query. If the answer is not in the context, say you don't know based on local data.
        
        Context:
        {context}
        
        Query: {query}
        
        Answer professionally:
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "No response from local model.")
            else:
                return f"Error: Local Ollama service returned {response.status_code}. Make sure Ollama is running."
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}"

if __name__ == "__main__":
    # Test stub
    pass

import os
import requests
import json

def publish_to_devto(article_path):
    api_key = os.getenv("DEVTO_API_KEY")
    if not api_key:
        # Check if it exists in a .env locally (though instructions say check .env)
        try:
            with open(".env", "r") as f:
                for line in f:
                    if line.startswith("DEVTO_API_KEY="):
                        api_key = line.split("=")[1].strip()
        except:
            pass
            
    if not api_key:
        print("[!] DEVTO_API_KEY not found. Cannot publish.")
        return

    with open(article_path, 'r') as f:
        content = f.read()

    # Extract title and tags from content or define them
    # For reliability, we send metadata in the payload
    # Standard format: { "article": { "title": "...", "body_markdown": "...", "published": true, "tags": [...] } }
    
    # Simple extraction for this script
    title = "TalentArch-AI: Building an Architectural Talent Matching Agent"
    tags = ["ai", "python", "rag", "recruitment"]
    
    payload = {
        "article": {
            "title": title,
            "body_markdown": content,
            "published": True,
            "tags": tags
        }
    }

    url = "https://dev.to/api/articles"
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 201:
        print(f"[v] Article published successfully!")
        print(f"URL: {response.json().get('url')}")
    else:
        print(f"[x] Error publishing: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    article_file = os.path.join(os.path.dirname(__file__), "..", "generated_article.md")
    publish_to_devto(article_file)

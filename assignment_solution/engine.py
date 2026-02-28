import requests
import time
from sentence_transformers import SentenceTransformer

class EndeeEngine:
    def __init__(self, host="http://localhost:8080", auth_token=""):
        self.host = host
        self.headers = {"Authorization": auth_token} if auth_token else {}
        # Using a reliable, lightweight model for 384-dimensional embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_name = "assignment_index"

    def ensure_index(self):
        """Checks if index exists, creates it if not."""
        try:
            # Check existing indexes
            res = requests.get(f"{self.host}/api/v1/index/list", headers=self.headers)
            if res.status_code == 200:
                existing = [idx['name'] for idx in res.json().get('data', [])]
                if self.index_name in existing:
                    return True
            
            # Create the index
            payload = {"name": self.index_name, "dimension": 384, "metric": "cosine"}
            requests.post(f"{self.host}/api/v1/index/create", json=payload, headers=self.headers)
            return True
        except Exception as e:
            print(f"Error connecting to Endee: {e}")
            return False

    def add_document(self, text):
        """Vectorize text and insert into Endee."""
        vector = self.model.encode(text).tolist()
        payload = {
            "index": self.index_name,
            "vectors": [vector],
            "metadata": [{"text": text, "timestamp": time.time()}]
        }
        start = time.time()
        requests.post(f"{self.host}/api/v1/vector/insert", json=payload, headers=self.headers)
        return time.time() - start

    def search(self, query):
        """Perform semantic search."""
        query_vector = self.model.encode(query).tolist()
        payload = {
            "index": self.index_name,
            "vector": query_vector,
            "top_k": 3
        }
        start = time.time()
        response = requests.post(f"{self.host}/api/v1/vector/search", json=payload, headers=self.headers)
        latency = (time.time() - start) * 1000
        
        results = response.json().get('data', []) if response.status_code == 200 else []
        return results, latency

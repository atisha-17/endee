import requests
import time
from sentence_transformers import SentenceTransformer

class EndeeEngine:
    def __init__(self, host="http://localhost:8080", auth_token=""):
        self.host = host
        self.headers = {"Authorization": auth_token} if auth_token else {}
        # This model turns text into a 384-dimensional vector
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_name = "intern_challenge_idx"

    def create_index(self):
        """Creates an index in Endee"""
        endpoint = f"{self.host}/api/v1/index/create" # Standard Endee API path
        payload = {
            "name": self.index_name,
            "dimension": 384,
            "metric": "cosine"
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        return response.status_code

    def add_document(self, text):
        """Vectorizes text and sends it to Endee"""
        vector = self.model.encode(text).tolist()
        endpoint = f"{self.host}/api/v1/vector/insert"
        payload = {
            "index": self.index_name,
            "vectors": [vector],
            "metadata": [{"text": text}]
        }
        start = time.time()
        requests.post(endpoint, json=payload, headers=self.headers)
        return time.time() - start

    def search(self, query):
        """Searches Endee for similar text"""
        query_vector = self.model.encode(query).tolist()
        endpoint = f"{self.host}/api/v1/vector/search"
        payload = {
            "index": self.index_name, 
            "vector": query_vector, 
            "top_k": 3
        }
        start = time.time()
        response = requests.post(endpoint, json=payload, headers=self.headers)
        latency = (time.time() - start) * 1000
        
        # Safely parse results
        results = response.json().get('data', []) if response.status_code == 200 else []
        return results, latency

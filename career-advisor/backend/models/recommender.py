
from typing import List, Dict
import json, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CareerRecommender:
    def __init__(self, data_path: str):
        with open(data_path, "r") as f:
            self.careers: List[Dict] = json.load(f)
        # Build corpus: combine title, skills, description, domain
        docs = []
        for c in self.careers:
            docs.append(" ".join([
                c["title"],
                c["domain"],
                " ".join(c["skills"]),
                c["description"]
            ]).lower())
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(docs)

    def recommend(self, profile_text: str, top_k: int = 3) -> List[Dict]:
        """profile_text is composed from quiz answers, interests, skills, values"""
        q = self.vectorizer.transform([profile_text.lower()])
        sims = cosine_similarity(q, self.matrix)[0]
        ranked = sorted(list(enumerate(sims)), key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for idx, score in ranked:
            item = dict(self.careers[idx])
            item["match_score"] = round(float(score), 3)
            results.append(item)
        return results

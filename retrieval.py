from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentRetriever:

    def __init__(self, documents):
        self.documents = documents

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.document_vectors = self.vectorizer.fit_transform(
            [doc["text"] for doc in documents]
        )

    def search(self, query, top_k=3):

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.document_vectors
        )[0]

        ranked_indices = scores.argsort()[::-1][:top_k]

        results = []

        for index in ranked_indices:
            results.append({
                "source": self.documents[index]["source"],
                "text": self.documents[index]["text"],
                "score": float(scores[index])
            })

        return results
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
import random
from collections import Counter

class BaseModel:
    """Base class for all IR models"""
    
    def __init__(self):
        self.name = "Base Model"
        
    def preprocess(self, text):
        """Simple preprocessing: lowercase and remove punctuation"""
        if not text:
            return ""
        return text.lower()
    
    def extract_snippet(self, content, query, max_length=150):
        """Extract a relevant snippet from the document content"""
        if len(content) <= max_length:
            return content
            
        # For simplicity, we'll just return the first part of the content
        # In a real system, this would identify the most relevant section
        return content[:max_length] + "..."
    
    def extract_keywords(self, text, top_n=15):
        """Extract keywords from text using TF-IDF approach"""
        # Initialize vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # Fit and transform the text
        try:
            tfidf_matrix = vectorizer.fit_transform([text])
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Get scores
            scores = tfidf_matrix.toarray()[0]
            
            # Create a dictionary of word->score
            word_scores = {word: score for word, score in zip(feature_names, scores)}
            
            # Get top N keywords
            top_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
            
            return [keyword for keyword, _ in top_keywords]
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def prepare_results(self, query, documents, scores_dict):
        sorted_ids = sorted(scores_dict.keys(), key=lambda x: scores_dict[x], reverse=True)
        results = []
        for doc_id in sorted_ids[:5]:  # Get top 5
            for doc in documents:
                if doc["id"] == doc_id:
                    extracted_keywords = self.extract_keywords(doc["content"], top_n=15)
                    results.append({
						"id": doc["id"],
						"title": doc["title"],
						"snippet": self.extract_snippet(doc["content"], query),
						"score": scores_dict[doc_id],
						"entities": extracted_keywords  # Use extracted keywords as entities
					})
                    break
        return results
        
    def search(self, query, documents):
        """Base search implementation - should be overridden"""
        raise NotImplementedError("Subclasses must implement search()")


class VectorIR(BaseModel):
    """Vector-based IR using TF-IDF representations"""
    
    def __init__(self):
        super().__init__()
        self.name = "Vector-based IR"
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def search(self, query, documents):
        """Search using Vector Space Model with TF-IDF weights"""
        # Ensure we have documents
        if not documents:
            return []
            
        # Preprocess the query
        processed_query = self.preprocess(query)
        
        # Extract and preprocess document content
        doc_contents = [self.preprocess(doc["content"]) for doc in documents]
        
        # Create document vectors
        try:
            # Fit vectorizer on document contents and transform
            doc_vectors = self.vectorizer.fit_transform(doc_contents)
            
            # Transform query to vector
            query_vector = self.vectorizer.transform([processed_query])
            
            # Calculate similarity scores using cosine similarity
            similarity_scores = cosine_similarity(query_vector, doc_vectors).flatten()
            
            # Create a dictionary of document IDs to scores
            scores_dict = {doc["id"]: float(score) for doc, score in zip(documents, similarity_scores)}
            
            # Prepare and return the results
            return self.prepare_results(query, documents, scores_dict)
            
        except Exception as e:
            print(f"Error in Vector IR search: {e}")
            return []


class LSA(BaseModel):
    """Latent Semantic Analysis-based retrieval"""
    
    def __init__(self):
        super().__init__()
        self.name = "LSA"
    
    def search(self, query, documents):
        """Search using LSA"""
        # In a real system, this would use SVD on the term-document matrix
        # For demo purposes, we'll simulate results with slight variations from Vector IR
        
        # First, get base similarity scores using TF-IDF approach
        vector_model = VectorIR()
        base_results = vector_model.search(query, documents)
        
        # Simulate some differences with LSA by slightly adjusting scores
        # LSA often captures more semantic relationships
        scores_dict = {}
        for doc in documents:
            # Base score from vector model
            base_score = next((res["score"] for res in base_results if res["id"] == doc["id"]), 0)
            
            # Adjust to simulate LSA behavior
            semantic_boost = 0
            query_terms = set(self.preprocess(query).split())
            
            # For each entity in the document that shares words with query, boost score
            for entity in doc["entities"]:
                entity_terms = set(self.preprocess(entity).split())
                if query_terms.intersection(entity_terms):
                    semantic_boost += 0.05

            # Apply the semantic boost with some randomness
            adjusted_score = min(1.0, base_score + semantic_boost + random.uniform(-0.1, 0.1))
            scores_dict[doc["id"]] = adjusted_score
        
        return self.prepare_results(query, documents, scores_dict)


class Word2Vec(BaseModel):
    """Word2Vec-based retrieval"""
    
    def __init__(self):
        super().__init__()
        self.name = "Word2Vec"
    
    def search(self, query, documents):
        """Search using Word2Vec embeddings"""
        # In a real system, this would use pre-trained Word2Vec embeddings
        # For demo purposes, we'll simulate results with variations from Vector IR
        
        # First, get base similarity scores using TF-IDF approach
        vector_model = VectorIR()
        base_results = vector_model.search(query, documents)
        
        # Simulate Word2Vec behavior by adjusting scores
        # Word2Vec often performs better on short texts and captures word-level semantics
        scores_dict = {}
        for doc in documents:
            # Base score from vector model
            base_score = next((res["score"] for res in base_results if res["id"] == doc["id"]), 0)
            
            # Adjust score based on document length (Word2Vec sometimes works better with shorter texts)
            length_factor = len(doc["content"].split()) / 100  # Normalize by 100 words
            length_adjustment = -0.05 * max(0, length_factor - 1)  # Slight penalty for longer docs
            
            # Word2Vec-like semantic matching (simulated)
            semantic_factor = random.uniform(-0.15, 0.15)  # Random variation to simulate semantic matching
            
            adjusted_score = min(1.0, max(0.1, base_score + length_adjustment + semantic_factor))
            scores_dict[doc["id"]] = adjusted_score
        
        return self.prepare_results(query, documents, scores_dict)


class GloVe(BaseModel):
    """GloVe-based retrieval"""
    
    def __init__(self):
        super().__init__()
        self.name = "GloVe"
    
    def search(self, query, documents):
        """Search using GloVe embeddings"""
        # In a real system, this would use pre-trained GloVe embeddings
        # For demo purposes, we'll simulate results with variations
        
        # First, get base similarity scores using TF-IDF approach
        vector_model = VectorIR()
        base_results = vector_model.search(query, documents)
        
        # Simulate GloVe behavior by adjusting scores
        # GloVe might capture different semantic patterns than Word2Vec
        scores_dict = {}
        for doc in documents:
            # Base score from vector model
            base_score = next((res["score"] for res in base_results if res["id"] == doc["id"]), 0)
            
            # GloVe-like adjustments (simulated)
            # Slightly different semantic matching pattern than Word2Vec
            semantic_factor = random.uniform(-0.1, 0.2)  # Random variation with slight positive bias
            
            # Simulate GloVe's better performance on certain content types
            title_weight = 0.05 if any(term in doc["title"].lower() for term in query.lower().split()) else 0
            
            adjusted_score = min(1.0, max(0.1, base_score + semantic_factor + title_weight))
            scores_dict[doc["id"]] = adjusted_score
        
        return self.prepare_results(query, documents, scores_dict)
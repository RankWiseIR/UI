from flask import Flask, request, jsonify, render_template, send_from_directory
import time
from models import VectorIR, LSA, Word2Vec, GloVe
# import os
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

# Initialize our models
vector_model = VectorIR()
lsa_model = LSA()
word2vec_model = Word2Vec()
glove_model = GloVe()

models = {
    'vector': vector_model,
    'lsa': lsa_model,
    'word2vec': word2vec_model,
    'glove': glove_model
}

# Sample document collection
documents = [
    {
        "id": 1,
        "title": "Understanding Vector Space Models in Information Retrieval",
        "content": "Vector space models represent documents and queries as vectors in high-dimensional space, enabling similarity calculations through measures like cosine similarity. This framework underpins many modern information retrieval systems, offering an intuitive geometric interpretation of document relevance.",
        # "entities": ["vector space", "information retrieval", "similarity", "cosine similarity"]
    },
    {
        "id": 2,
        "title": "Comparing Embedding Techniques for Document Retrieval",
        "content": "This paper presents a comprehensive analysis of embedding techniques including Word2Vec, GloVe and LSA for document retrieval tasks. We evaluate their performance across multiple datasets and demonstrate that contextual embeddings consistently outperform traditional approaches in capturing semantic relationships.",
        "entities": ["embedding", "Word2Vec", "GloVe", "LSA", "semantic"]
    },
    {
        "id": 3,
        "title": "Recent Advances in Neural Information Retrieval",
        "content": "Neural networks have revolutionized information retrieval by learning representations that capture semantic relationships between queries and documents. Transformer-based models like BERT have established new state-of-the-art results for retrieval tasks by leveraging contextual understanding and attention mechanisms.",
        "entities": ["neural networks", "semantic", "information retrieval", "transformer", "BERT"]
    },
    {
        "id": 4,
        "title": "Optimizing Search Performance in Large Document Collections",
        "content": "Efficient indexing strategies and retrieval algorithms are crucial for maintaining performance as document collections grow. This paper explores techniques like inverted indices, approximate nearest neighbor search, and query optimization that enable sub-linear search time in massive document stores.",
        "entities": ["indexing", "performance", "algorithms", "inverted indices", "nearest neighbor"]
    },
    {
        "id": 5,
        "title": "Evaluation Metrics for Information Retrieval Systems",
        "content": "This survey covers key evaluation metrics including precision, recall, F1-score, MRR, and NDCG with practical examples. We discuss the trade-offs between different metrics and provide guidelines for selecting appropriate evaluation criteria based on retrieval system goals and user requirements.",
        "entities": ["evaluation", "metrics", "precision", "recall", "NDCG", "MRR"]
    },
    {
        "id": 6,
        "title": "The Role of Query Expansion in Modern Search Engines",
        "content": "Query expansion techniques augment the original query with related terms to improve recall and address vocabulary mismatch problems. This paper examines approaches ranging from traditional thesaurus-based methods to newer neural models that leverage contextual similarity for identifying expansion candidates.",
        "entities": ["query expansion", "recall", "vocabulary mismatch", "thesaurus", "contextual similarity"]
    },
    {
        "id": 7,
        "title": "Cross-Lingual Information Retrieval Challenges",
        "content": "Cross-lingual IR systems face unique challenges in bridging language barriers between queries and documents. We review multilingual embedding approaches, translation techniques, and language-agnostic retrieval models that enable effective search across linguistically diverse document collections.",
        "entities": ["cross-lingual", "multilingual", "embeddings", "translation", "language-agnostic"]
    },
    {
        "id": 8,
        "title": "Personalized Search: Adapting Results to User Context",
        "content": "Personalized search systems tailor results based on user preferences, search history, and contextual factors. This paper discusses techniques for building user models, incorporating implicit feedback, and balancing personalization with privacy concerns in modern retrieval systems.",
        "entities": ["personalized search", "user context", "user models", "implicit feedback", "privacy"]
    },
    {
        "id": 9,
        "title": "Explainable Information Retrieval",
        "content": "Transparency in search results helps users understand why specific documents were retrieved. This survey examines methods for generating explanations in IR systems, from simple feature importance approaches to more sophisticated attention visualization and counterfactual reasoning techniques.",
        "entities": ["explainable", "transparency", "feature importance", "attention visualization", "counterfactual"]
    },
    {
        "id": 10,
        "title": "Entity-Centric Information Retrieval",
        "content": "Entity-centric retrieval focuses on returning structured information about specific entities rather than just documents. This approach leverages knowledge graphs, entity linking, and attribute extraction to enable more precise answers to entity-oriented queries in search systems.",
        "entities": ["entity-centric", "knowledge graphs", "entity linking", "attribute extraction", "structured information"]
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search')
def search():
    query = request.args.get('query', '')
    model_name = request.args.get('model', 'vector')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    if model_name not in models:
        return jsonify({'error': 'Invalid model name'}), 400
    
    model = models[model_name]
    
    # Record start time for performance metrics
    start_time = time.time()
    
    # Pre-extract keywords from the query to use for result relevance
    query_keywords = model.extract_keywords(query)
    print(f"Query keywords: {query_keywords}")
    
    # Get the model results
    results = model.search(query, documents)
    
    # Calculate retrieval time
    retrieval_time = time.time() - start_time
    
    # Calculate metrics 
    np.random.seed(hash(query + model_name) % 2**32)
    
    # Mock metrics 
    metrics = {
        'precision': min(1.0, max(0.6, 0.8 + np.random.normal(0, 0.1))),
        'recall': min(1.0, max(0.5, 0.7 + np.random.normal(0, 0.1))),
        'f1_score': min(1.0, max(0.6, 0.75 + np.random.normal(0, 0.1))),
        'mean_reciprocal_rank': min(1.0, max(0.5, 0.65 + np.random.normal(0, 0.15))),
        'ndcg': min(1.0, max(0.6, 0.75 + np.random.normal(0, 0.1)))
    }
    
    # response
    response = {
        'model': model_name,
        'query': query,
        'query_keywords': query_keywords,
        'time_taken': round(retrieval_time, 3),
        'metrics': metrics,
        'results': results
    }
    
    return jsonify(response)


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5001)
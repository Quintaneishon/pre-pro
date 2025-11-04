"""
Simple Word Tokenizer and Text Search Module
Handles Spanish text tokenization, vectorization, and search functionality
"""

import os
import re
import string
from collections import Counter
from typing import List, Dict, Tuple
import numpy as np
from pathlib import Path


class SimpleTokenizer:
    """Simple word tokenizer for Spanish text"""
    
    # Spanish stopwords
    STOPWORDS = {
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
        'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
        'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
        'la', 'si', 'me', 'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy',
        'sin', 'vez', 'mucho', 'saber', 'qué', 'sobre', 'mi', 'alguno', 'mismo',
        'yo', 'también', 'hasta', 'año', 'dos', 'querer', 'entre', 'así', 'primero',
        'desde', 'grande', 'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella',
        'sí', 'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa',
        'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora', 'parte',
        'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar', 'llevar', 'dejar',
        'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar', 'algo', 'solo',
        'decir', 'casa', 'mundo', 'país', 'últimos', 'contra', 'venir', 'este',
        'trabajo', 'cual', 'fue', 'han', 'son', 'es', 'del', 'las', 'los', 'al',
        'una', 'cuál', 'cómo', 'qué', 'cuántos', 'cuántas', 'fue', 'fueron',
        'ha', 'hay', 'tiene', 'tienen', 'tuvo', 'tuvieron'
    }
    
    def __init__(self, remove_stopwords=True, min_word_length=3):
        self.remove_stopwords = remove_stopwords
        self.min_word_length = min_word_length
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text string
            
        Returns:
            List of tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation and special characters
        text = re.sub(f'[{re.escape(string.punctuation)}]', ' ', text)
        
        # Split into words
        words = text.split()
        
        # Filter words
        tokens = []
        for word in words:
            # Skip if too short
            if len(word) < self.min_word_length:
                continue
            
            # Skip if stopword
            if self.remove_stopwords and word in self.STOPWORDS:
                continue
            
            # Skip if only numbers
            if word.isdigit():
                continue
            
            tokens.append(word)
        
        return tokens
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Extract top keywords from text
        
        Args:
            text: Input text
            top_n: Number of top keywords to return
            
        Returns:
            List of (word, frequency) tuples
        """
        tokens = self.tokenize(text)
        counter = Counter(tokens)
        return counter.most_common(top_n)


class TFIDFVectorizer:
    """Simple TF-IDF vectorizer"""
    
    def __init__(self, tokenizer: SimpleTokenizer):
        self.tokenizer = tokenizer
        self.vocabulary = {}
        self.idf = {}
        self.documents = []
    
    def fit(self, documents: List[str]):
        """
        Fit the vectorizer on documents
        
        Args:
            documents: List of text documents
        """
        self.documents = documents
        
        # Tokenize all documents
        tokenized_docs = [self.tokenizer.tokenize(doc) for doc in documents]
        
        # Build vocabulary
        all_words = set()
        for tokens in tokenized_docs:
            all_words.update(tokens)
        
        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}
        
        # Calculate IDF
        n_docs = len(documents)
        for word in self.vocabulary:
            # Count documents containing the word
            doc_count = sum(1 for tokens in tokenized_docs if word in tokens)
            # IDF formula: log(N / (1 + df))
            self.idf[word] = np.log(n_docs / (1 + doc_count))
    
    def transform(self, text: str) -> np.ndarray:
        """
        Transform text to TF-IDF vector
        
        Args:
            text: Input text
            
        Returns:
            TF-IDF vector as numpy array
        """
        tokens = self.tokenizer.tokenize(text)
        token_counts = Counter(tokens)
        
        # Initialize vector
        vector = np.zeros(len(self.vocabulary))
        
        # Calculate TF-IDF for each word
        total_tokens = len(tokens)
        for word, count in token_counts.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                tf = count / total_tokens if total_tokens > 0 else 0
                idf = self.idf.get(word, 0)
                vector[idx] = tf * idf
        
        return vector
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class TextSearchEngine:
    """Search engine for text files"""
    
    def __init__(self, text_dir: str):
        """
        Initialize search engine
        
        Args:
            text_dir: Directory containing text files
        """
        self.text_dir = Path(text_dir)
        self.tokenizer = SimpleTokenizer()
        self.vectorizer = TFIDFVectorizer(self.tokenizer)
        self.documents = []
        self.filenames = []
        self._load_documents()
    
    def _load_documents(self):
        """Load all text documents from directory"""
        text_files = sorted(self.text_dir.glob('*.txt'))
        
        for file_path in text_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.documents.append(content)
                    self.filenames.append(file_path.name)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        print(f"Loaded {len(self.documents)} documents")
        
        # Fit vectorizer
        if self.documents:
            self.vectorizer.fit(self.documents)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for documents matching the query
        
        Args:
            query: Search query text
            top_k: Number of top results to return
            
        Returns:
            List of results with filename, score, and snippet
        """
        # Vectorize query
        query_vector = self.vectorizer.transform(query)
        
        # Calculate similarity with all documents
        scores = []
        for doc in self.documents:
            doc_vector = self.vectorizer.transform(doc)
            similarity = self.vectorizer.cosine_similarity(query_vector, doc_vector)
            scores.append(similarity)
        
        # Get top results
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        query_keywords = self.tokenizer.tokenize(query)
        
        for idx in top_indices:
            if scores[idx] > 0:  # Only include non-zero scores
                # Extract snippet with keywords
                snippet = self._extract_snippet(
                    self.documents[idx], 
                    query_keywords
                )
                
                results.append({
                    'filename': self.filenames[idx],
                    'score': float(scores[idx]),
                    'snippet': snippet
                })
        
        return results
    
    def _extract_snippet(self, document: str, keywords: List[str], 
                        context_chars: int = 200) -> str:
        """
        Extract relevant snippet from document
        
        Args:
            document: Full document text
            keywords: List of keywords to search for
            context_chars: Number of characters of context
            
        Returns:
            Text snippet
        """
        document_lower = document.lower()
        
        # Find first occurrence of any keyword
        best_pos = -1
        for keyword in keywords:
            pos = document_lower.find(keyword)
            if pos != -1 and (best_pos == -1 or pos < best_pos):
                best_pos = pos
        
        if best_pos == -1:
            # No keyword found, return beginning
            return document[:context_chars] + "..."
        
        # Extract context around keyword
        start = max(0, best_pos - context_chars // 2)
        end = min(len(document), best_pos + context_chars // 2)
        
        snippet = document[start:end]
        
        # Add ellipsis if needed
        if start > 0:
            snippet = "..." + snippet
        if end < len(document):
            snippet = snippet + "..."
        
        return snippet.strip()
    
    def extract_query_keywords(self, query: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Extract keywords from query
        
        Args:
            query: Query text
            top_n: Number of keywords to extract
            
        Returns:
            List of (keyword, frequency) tuples
        """
        return self.tokenizer.extract_keywords(query, top_n)


# Example usage
if __name__ == "__main__":
    # Example
    text_dir = "../data/text"
    search_engine = TextSearchEngine(text_dir)
    
    query = "¿Cuál fue la evolución del número de casos confirmados por año?"
    results = search_engine.search(query, top_k=5)
    
    print(f"Query: {query}\n")
    print(f"Keywords: {search_engine.extract_query_keywords(query)}\n")
    
    for i, result in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  File: {result['filename']}")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Snippet: {result['snippet'][:150]}...")
        print()


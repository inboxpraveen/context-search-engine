import faiss
import numpy as np

import pickle

import torch
from transformers import DistilBertTokenizer, DistilBertModel


# GLOBAL CONSTANTS
MODEL_PATH = 'distilbert-base-uncased'
DIMENSION = 768
INDEX_PATH = "faiss_index.idx"
CHUNK_MAPPING_PATH = "index_to_chunk.pkl"


# 1. Initialize DistilBERT
TOKENIZER = DistilBertTokenizer.from_pretrained(MODEL_PATH)
MODEL = DistilBertModel.from_pretrained(MODEL_PATH)


def get_embedding(text, pooling='mean'):
    """
    Compute the embeddings for a given text using DistilBert.
    
    Parameters:
    - text (str): The text for which embeddings are to be generated.
    - pooling (str, optional): The type of pooling to be applied. 
                               Can be 'mean', 'max', or 'mean_max'. 
                               Defaults to 'mean'.
                               
    Returns:
    - numpy.ndarray: The computed embedding.
    
    Pooling Techniques Explained:
    --------------------------------
    Pooling is a technique to aggregate a sequence of embeddings into a single embedding vector. 
    Given a text with N tokens, we get an NxD matrix of embeddings (D is the embedding dimension). 
    To transform this into a 1xD embedding, we use pooling. Here's how each technique works:

    - Mean Pooling:
        We take the average of all embeddings in the sequence.
        Example: For embeddings [2, 4, 6] and [3, 6, 9], mean pooling results in [2.5, 5, 7.5].

    - Max Pooling:
        We take the maximum value in each dimension across all embeddings in the sequence.
        Example: For embeddings [2, 4, 6] and [3, 6, 9], max pooling results in [3, 6, 9].

    - Min Pooling:
        We take the minimum value in each dimension across all embeddings in the sequence.
        Example: For embeddings [2, 4, 6] and [3, 6, 9], min pooling results in [2, 4, 6].
    
    Example:
    >>> embedding = get_embedding("Hello, world!")
    >>> print(embedding.shape)
    (1, 768)
    """
    input_ids = TOKENIZER.encode(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        output = MODEL(input_ids)
    if pooling == 'mean':
        return output.last_hidden_state.mean(dim=1).numpy()
    elif pooling == 'max':
        return output.last_hidden_state.max(dim=1).numpy()
    elif pooling == 'mean_max':
        mean_pooled = output.last_hidden_state.mean(dim=1).numpy()
        max_pooled = output.last_hidden_state.max(dim=1).numpy()
        return np.concatenate([mean_pooled, max_pooled], axis=1)


def search_in_index(query, num_matches=1):
    """
    Search for the most relevant chunk in the FAISS index based on a query.
    
    Parameters:
    - query (str): The query string for which a matching chunk is to be found.
    - num_matches (int, optional): The number of matches to retrieve. 
                                   Defaults to 1.
                                   
    Returns:
    - str: The matched paragraph.
    
    Example:
    >>> result = search_in_index("Introduction to AI")
    >>> print(result)
    ... # Output: Relevant chunk from indexed documents.
    """
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "rb") as f:
        index_to_chunk = pickle.load(f)
    
    vector = get_embedding(query)
    D, I = index.search(vector.reshape(1, DIMENSION), num_matches)
    matched_paragraph = index_to_chunk[I[0][0]]
    return matched_paragraph

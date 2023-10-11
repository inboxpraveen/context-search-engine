import os
import pickle

import faiss
import numpy as np

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import torch
from transformers import DistilBertTokenizer, DistilBertModel


# GLOBAL CONSTANTS
MODEL_PATH = 'distilbert-base-uncased'
DIMENSION = 768
NLIST = 2
INDEX_PATH = "faiss_index.idx"
CHUNK_MAPPING_PATH = "index_to_chunk.pkl"
MAX_CHUNK_SIZE = 64


# Initialization of model
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


def chunk_document(document, max_size=MAX_CHUNK_SIZE):
    """
    Split the document into smaller chunks of maximum size.
    
    Parameters:
    - document (str): The text document to be split.
    - max_size (int, optional): The maximum number of words per chunk. 
                                Defaults to MAX_CHUNK_SIZE.
                                
    Yields:
    - str: Chunks of the document.
    
    Example:
    >>> chunks = list(chunk_document("This is a sample document with more than eight words."))
    >>> for chunk in chunks:
    ...     print(chunk)
    ...
    This is a sample document with more
    than eight words.
    """
    words = document.split()
    for i in range(0, len(words), max_size):
        yield ' '.join(words[i:i+max_size])


def preprocess_text(text):
    return ' '.join([word for word in text.lower().split() if word not in ENGLISH_STOP_WORDS])


def create_faiss_index(folder_path):
    """
    Create and save a FAISS index for all the documents in the provided folder.
    
    Parameters:
    - folder_path (str): Path to the folder containing the .txt documents.
    
    Writes:
    - An index file (faiss_index.idx) and a mapping file (index_to_chunk.pkl) to disk.
    
    Example:
    >>> create_faiss_index('./docs/')
    >>> # This will generate 'faiss_index.idx' and 'index_to_chunk.pkl'
    """

    index_to_chunk = {}

    quantizer = faiss.IndexHNSWFlat(DIMENSION, 32)
    index = faiss.IndexIVFFlat(quantizer, DIMENSION, NLIST, faiss.METRIC_L2)
    
    all_embeddings = []
    all_chunks = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding="utf-8") as f:
                content = preprocess_text(f.read())
                for chunk in chunk_document(content):
                    embedding = get_embedding(chunk)
                    all_embeddings.append(embedding)
                    all_chunks.append(chunk)
                    
    embeddings_np = np.vstack(all_embeddings)
    faiss.normalize_L2(embeddings_np)
    index.train(embeddings_np)
    
    for i, embedding in enumerate(all_embeddings):
        index.add(embedding)
        index_to_chunk[i] = all_chunks[i]
    
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "wb") as f:
        pickle.dump(index_to_chunk, f)


if __name__ == "__main__":
    folder_path = './docs/'
    create_faiss_index(folder_path)

import faiss
import torch
import pickle
from transformers import DistilBertTokenizer, DistilBertModel
import numpy as np

# 1. Initialize DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def get_embedding(text, pooling='mean'):
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        output = model(input_ids)
    if pooling == 'mean':
        return output.last_hidden_state.mean(dim=1).numpy()
    elif pooling == 'max':
        return output.last_hidden_state.max(dim=1).numpy()
    elif pooling == 'mean_max':
        mean_pooled = output.last_hidden_state.mean(dim=1).numpy()
        max_pooled = output.last_hidden_state.max(dim=1).numpy()
        return np.concatenate([mean_pooled, max_pooled], axis=1)

# 4. Highlight the context in the paragraph
def highlight_context(document, query):
    words = query.split()
    for word in words:
        document = document.replace(word, f"<mark>{word}</mark>")
    return document

def search_in_index(query, num_matches=1):
    index = faiss.read_index("faiss_index.idx")
    with open("index_to_chunk.pkl", "rb") as f:
        index_to_chunk = pickle.load(f)
    
    vector = get_embedding(query)
    D, I = index.search(vector.reshape(1, 768), num_matches)
    matched_paragraph = index_to_chunk[I[0][0]]
    highlighted_paragraph = highlight_context(matched_paragraph, query)
    return highlighted_paragraph

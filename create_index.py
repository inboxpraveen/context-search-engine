import os
import faiss
import pickle
import torch
import numpy as np
from transformers import DistilBertTokenizer, DistilBertModel


# Initialization of model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# 1. Function to generate embeddings
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


# 2. Chunk the document into max_size
def chunk_document(document, max_size=64):
    words = document.split()
    for i in range(0, len(words), max_size):
        yield ' '.join(words[i:i+max_size])

# For maintaining index to each document.
index_to_chunk = {}


# 3. Creating FAISS Index for all the documents
def create_faiss_index(folder_path):
    dimension = 768
    quantizer = faiss.IndexFlatL2(dimension)
    # nlist = min(100, len(embeddings))
    nlist = 2
    index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_L2)

    # Need to train the index before adding data
    embeddings = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding="utf-8") as f:
                content = f.read()
                for chunk in chunk_document(content):
                    embedding = get_embedding(chunk)
                    embeddings.append(embedding)

    embeddings_np = np.vstack(embeddings)
    faiss.normalize_L2(embeddings_np)
    index.train(embeddings_np)
    
    current_index = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding="utf-8") as f:
                content = f.read()
                for chunk in chunk_document(content):
                    embedding = get_embedding(chunk)
                    index.add(embedding)
                    index_to_chunk[current_index] = chunk
                    current_index += 1

    faiss.write_index(index, "faiss_index.idx")
    with open("index_to_chunk.pkl", "wb") as f:
        pickle.dump(index_to_chunk, f)


if __name__ == "__main__":
    folder_path = './docs/'
    create_faiss_index(folder_path)

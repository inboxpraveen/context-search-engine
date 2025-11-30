import os
import pickle
import faiss
import numpy as np
import torch
import shutil
from datetime import datetime
from transformers import DistilBertTokenizer, DistilBertModel
from PyPDF2 import PdfReader
from docx import Document

MODEL_PATH = 'distilbert-base-uncased'
DIMENSION = 768
INDEX_PATH = "faiss_index.idx"
CHUNK_MAPPING_PATH = "index_to_chunk.pkl"
METADATA_PATH = "document_metadata.pkl"
UPLOAD_BASE_DIR = "uploads"

TOKENIZER = DistilBertTokenizer.from_pretrained(MODEL_PATH)
MODEL = DistilBertModel.from_pretrained(MODEL_PATH)


def get_embedding(text, pooling='mean'):
    input_ids = TOKENIZER.encode(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        output = MODEL(input_ids)
    if pooling == 'mean':
        return output.last_hidden_state.mean(dim=1).numpy()
    elif pooling == 'max':
        return output.last_hidden_state.max(dim=1)[0].numpy()
    return output.last_hidden_state.mean(dim=1).numpy()


def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_text_from_docx(file_path):
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text


def extract_text_from_txt(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
    return text


def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    return ""


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def initialize_or_load_index():
    if os.path.exists(INDEX_PATH) and os.path.exists(CHUNK_MAPPING_PATH):
        index = faiss.read_index(INDEX_PATH)
        with open(CHUNK_MAPPING_PATH, "rb") as f:
            index_to_chunk = pickle.load(f)
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, "rb") as f:
                metadata = pickle.load(f)
        else:
            metadata = {"documents": [], "total_chunks": 0}
    else:
        index = faiss.IndexFlatL2(DIMENSION)
        index_to_chunk = {}
        metadata = {"documents": [], "total_chunks": 0}
    return index, index_to_chunk, metadata


def add_document_to_index(file_path, filename, original_filename):
    text = extract_text_from_file(file_path)
    if not text.strip():
        return False, "Could not extract text from document", None
    
    chunks = chunk_text(text)
    if not chunks:
        return False, "No content to index", None
    
    index, index_to_chunk, metadata = initialize_or_load_index()
    
    start_idx = len(index_to_chunk)
    embeddings = []
    
    timestamp = datetime.now()
    doc_id = f"doc_{timestamp.strftime('%Y%m%d_%H%M%S')}_{len(metadata['documents'])}"
    
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
        index_to_chunk[start_idx + i] = {
            "text": chunk,
            "document": original_filename,
            "doc_id": doc_id,
            "chunk_index": i
        }
    
    embeddings_array = np.vstack(embeddings).astype('float32')
    index.add(embeddings_array)
    
    file_ext = os.path.splitext(original_filename)[1].lower()
    doc_type = "PDF" if file_ext == ".pdf" else "Word" if file_ext == ".docx" else "Text"
    
    doc_metadata = {
        "id": doc_id,
        "filename": original_filename,
        "path": file_path,
        "chunks": len(chunks),
        "uploaded_on": timestamp.isoformat(),
        "type": doc_type,
        "size": os.path.getsize(file_path)
    }
    
    metadata["documents"].append(doc_metadata)
    metadata["total_chunks"] = len(index_to_chunk)
    
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "wb") as f:
        pickle.dump(index_to_chunk, f)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
    
    return True, f"Successfully indexed {len(chunks)} chunks from {original_filename}", doc_id


def get_metadata():
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "rb") as f:
            return pickle.load(f)
    return {"documents": [], "total_chunks": 0}


def delete_document(doc_id):
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNK_MAPPING_PATH):
        return False, "No index found"
    
    index, index_to_chunk, metadata = initialize_or_load_index()
    
    doc_to_delete = None
    for doc in metadata["documents"]:
        if doc["id"] == doc_id:
            doc_to_delete = doc
            break
    
    if not doc_to_delete:
        return False, "Document not found"
    
    new_index = faiss.IndexFlatL2(DIMENSION)
    new_index_to_chunk = {}
    new_idx = 0
    embeddings_to_keep = []
    
    for idx, chunk_data in index_to_chunk.items():
        if chunk_data.get("doc_id") != doc_id:
            new_index_to_chunk[new_idx] = chunk_data
            vector = get_embedding(chunk_data["text"])
            embeddings_to_keep.append(vector)
            new_idx += 1
    
    if embeddings_to_keep:
        embeddings_array = np.vstack(embeddings_to_keep).astype('float32')
        new_index.add(embeddings_array)
    
    metadata["documents"] = [doc for doc in metadata["documents"] if doc["id"] != doc_id]
    metadata["total_chunks"] = len(new_index_to_chunk)
    
    if os.path.exists(doc_to_delete["path"]):
        try:
            os.remove(doc_to_delete["path"])
        except:
            pass
    
    faiss.write_index(new_index, INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "wb") as f:
        pickle.dump(new_index_to_chunk, f)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
    
    return True, f"Successfully deleted {doc_to_delete['filename']}"


def get_document_content(doc_id):
    metadata = get_metadata()
    for doc in metadata["documents"]:
        if doc["id"] == doc_id:
            if os.path.exists(doc["path"]):
                text = extract_text_from_file(doc["path"])
                return {"filename": doc["filename"], "content": text, "type": doc["type"]}
    return None


def search_in_index(query, num_matches=3):
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNK_MAPPING_PATH):
        return []
    
    if not query or not query.strip():
        return []
    
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "rb") as f:
        index_to_chunk = pickle.load(f)
    
    if len(index_to_chunk) == 0:
        return []
    
    vector = get_embedding(query)
    D, I = index.search(vector.reshape(1, DIMENSION), min(num_matches, len(index_to_chunk)))
    
    results = []
    for i, idx in enumerate(I[0]):
        if idx < len(index_to_chunk):
            chunk_data = index_to_chunk[idx]
            results.append({
                "text": chunk_data["text"] if isinstance(chunk_data, dict) else chunk_data,
                "document": chunk_data.get("document", "Unknown") if isinstance(chunk_data, dict) else "Unknown",
                "score": float(D[0][i])
            })
    
    return results


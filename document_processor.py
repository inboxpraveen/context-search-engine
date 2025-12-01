import os
import pickle
import faiss
import numpy as np
import torch
from datetime import datetime
from transformers import AutoTokenizer, AutoModel
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
from config import load_config

INDEX_PATH = "faiss_index.idx"
CHUNK_MAPPING_PATH = "index_to_chunk.pkl"
METADATA_PATH = "document_metadata.pkl"
UPLOAD_BASE_DIR = "uploads"

# Global model cache
_model_cache = {}
_tokenizer_cache = {}


def get_model_and_tokenizer(model_name=None):
    """Get or load model and tokenizer with caching"""
    if model_name is None:
        config = load_config()
        model_name = config.get("model_repo_id", "distilbert-base-uncased")
    
    if model_name not in _model_cache:
        try:
            _tokenizer_cache[model_name] = AutoTokenizer.from_pretrained(model_name)
            _model_cache[model_name] = AutoModel.from_pretrained(model_name)
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            # Fallback to default
            model_name = "distilbert-base-uncased"
            _tokenizer_cache[model_name] = AutoTokenizer.from_pretrained(model_name)
            _model_cache[model_name] = AutoModel.from_pretrained(model_name)
    
    return _tokenizer_cache[model_name], _model_cache[model_name]


def get_embedding(text, pooling='mean'):
    """Generate embeddings using configured model"""
    tokenizer, model = get_model_and_tokenizer()
    
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        output = model(input_ids)
    
    if pooling == 'mean':
        return output.last_hidden_state.mean(dim=1).numpy()
    elif pooling == 'max':
        return output.last_hidden_state.max(dim=1)[0].numpy()
    
    return output.last_hidden_state.mean(dim=1).numpy()


def extract_text_from_pdf(file_path):
    """Extract text from PDF with page tracking"""
    pages_text = []
    try:
        reader = PdfReader(file_path)
        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                pages_text.append({
                    'page_number': page_num,
                    'text': page_text
                })
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return pages_text


def extract_text_from_docx(file_path):
    """Extract text from DOCX (no page concept, use sections)"""
    text = ""
    try:
        doc = DocxDocument(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return [{'page_number': 1, 'text': text}]


def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
    return [{'page_number': 1, 'text': text}]


def extract_text_from_file(file_path):
    """Extract text from file based on extension"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    return []


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks with overlap"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def initialize_or_load_index():
    """Initialize or load existing FAISS index"""
    config = load_config()
    dimension = config.get("dimension", 768)
    
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
        index = faiss.IndexFlatL2(dimension)
        index_to_chunk = {}
        metadata = {"documents": [], "total_chunks": 0}
    
    return index, index_to_chunk, metadata


def add_document_to_index(file_path, filename, original_filename):
    """Add document to index with enhanced metadata"""
    config = load_config()
    chunk_size = config.get("chunk_size", 500)
    overlap = config.get("chunk_overlap", 50)
    
    pages_text = extract_text_from_file(file_path)
    if not pages_text:
        return False, "Could not extract text from document", None
    
    index, index_to_chunk, metadata = initialize_or_load_index()
    
    start_idx = len(index_to_chunk)
    embeddings = []
    
    timestamp = datetime.now()
    doc_id = f"doc_{timestamp.strftime('%Y%m%d_%H%M%S')}_{len(metadata['documents'])}"
    
    chunk_counter = 0
    
    # Process each page
    for page_data in pages_text:
        page_num = page_data['page_number']
        page_text = page_data['text']
        
        # Chunk the page text
        page_chunks = chunk_text(page_text, chunk_size, overlap)
        
        for chunk in page_chunks:
            embedding = get_embedding(chunk)
            embeddings.append(embedding)
            
            index_to_chunk[start_idx + chunk_counter] = {
                "text": chunk,
                "document": original_filename,
                "doc_id": doc_id,
                "chunk_index": chunk_counter,
                "page_number": page_num
            }
            chunk_counter += 1
    
    if len(embeddings) == 0:
        return False, "No content to index", None
    
    embeddings_array = np.vstack(embeddings).astype('float32')
    index.add(embeddings_array)
    
    file_ext = os.path.splitext(original_filename)[1].lower()
    doc_type = "PDF" if file_ext == ".pdf" else "Word" if file_ext == ".docx" else "Text"
    
    doc_metadata = {
        "id": doc_id,
        "filename": original_filename,
        "path": file_path,
        "chunks": chunk_counter,
        "uploaded_on": timestamp.isoformat(),
        "type": doc_type,
        "size": os.path.getsize(file_path),
        "pages": len(pages_text)
    }
    
    metadata["documents"].append(doc_metadata)
    metadata["total_chunks"] = len(index_to_chunk)
    
    # Save
    faiss.write_index(index, INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "wb") as f:
        pickle.dump(index_to_chunk, f)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
    
    return True, f"Successfully indexed {chunk_counter} chunks from {original_filename}", doc_id


def delete_document(doc_id):
    """Delete document and rebuild index"""
    config = load_config()
    dimension = config.get("dimension", 768)
    
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
    
    new_index = faiss.IndexFlatL2(dimension)
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
    """Get full document content"""
    metadata = get_metadata()
    for doc in metadata["documents"]:
        if doc["id"] == doc_id:
            if os.path.exists(doc["path"]):
                pages_text = extract_text_from_file(doc["path"])
                full_text = "\n\n".join([page['text'] for page in pages_text])
                return {
                    "filename": doc["filename"],
                    "content": full_text,
                    "type": doc["type"],
                    "pages": doc.get("pages", 1)
                }
    return None


def search_in_index(query, num_matches=5, sort_by="relevance"):
    """Search index with sorting options"""
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNK_MAPPING_PATH):
        return []
    
    if not query or not query.strip():
        return []
    
    index = faiss.read_index(INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "rb") as f:
        index_to_chunk = pickle.load(f)
    
    if len(index_to_chunk) == 0:
        return []
    
    config = load_config()
    top_k = config.get("top_k", 10)
    
    vector = get_embedding(query)
    D, I = index.search(vector.reshape(1, -1), min(top_k, len(index_to_chunk)))
    
    results = []
    metadata = get_metadata()
    
    for i, idx in enumerate(I[0]):
        if idx < len(index_to_chunk):
            chunk_data = index_to_chunk[idx]
            
            # Find document upload date
            upload_date = None
            for doc in metadata.get("documents", []):
                if doc["id"] == chunk_data.get("doc_id"):
                    upload_date = doc.get("uploaded_on")
                    break
            
            results.append({
                "text": chunk_data["text"],
                "document": chunk_data.get("document", "Unknown"),
                "doc_id": chunk_data.get("doc_id"),
                "page_number": chunk_data.get("page_number", 1),
                "chunk_number": chunk_data.get("chunk_index", 0) + 1,
                "score": float(D[0][i]),
                "uploaded_on": upload_date
            })
    
    # Sort results
    if sort_by == "recent":
        results.sort(key=lambda x: x.get("uploaded_on", ""), reverse=True)
    # Default is by relevance (already sorted by FAISS)
    
    return results[:num_matches]


def get_metadata():
    """Get document metadata"""
    if os.path.exists(METADATA_PATH):
        with open(METADATA_PATH, "rb") as f:
            return pickle.load(f)
    return {"documents": [], "total_chunks": 0}


def rebuild_index_with_new_config():
    """Rebuild entire index with new configuration (for model changes)"""
    metadata = get_metadata()
    config = load_config()
    dimension = config.get("dimension", 768)
    
    if len(metadata.get("documents", [])) == 0:
        return True, "No documents to reindex"
    
    # Create new index
    new_index = faiss.IndexFlatL2(dimension)
    new_index_to_chunk = {}
    chunk_counter = 0
    embeddings = []
    
    for doc in metadata["documents"]:
        if not os.path.exists(doc["path"]):
            continue
        
        pages_text = extract_text_from_file(doc["path"])
        
        for page_data in pages_text:
            page_num = page_data['page_number']
            page_text = page_data['text']
            
            page_chunks = chunk_text(
                page_text,
                config.get("chunk_size", 500),
                config.get("chunk_overlap", 50)
            )
            
            for idx, chunk in enumerate(page_chunks):
                embedding = get_embedding(chunk)
                embeddings.append(embedding)
                
                new_index_to_chunk[chunk_counter] = {
                    "text": chunk,
                    "document": doc["filename"],
                    "doc_id": doc["id"],
                    "chunk_index": chunk_counter,
                    "page_number": page_num
                }
                chunk_counter += 1
    
    if embeddings:
        embeddings_array = np.vstack(embeddings).astype('float32')
        new_index.add(embeddings_array)
    
    metadata["total_chunks"] = len(new_index_to_chunk)
    
    # Save new index
    faiss.write_index(new_index, INDEX_PATH)
    with open(CHUNK_MAPPING_PATH, "wb") as f:
        pickle.dump(new_index_to_chunk, f)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)
    
    return True, f"Reindexed {len(metadata['documents'])} documents with {chunk_counter} chunks"

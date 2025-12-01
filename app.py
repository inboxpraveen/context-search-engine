import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from document_processor import (
    add_document_to_index, 
    search_in_index, 
    get_metadata,
    delete_document,
    get_document_content,
    rebuild_index_with_new_config
)
from config import load_config, save_config, get_version

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_path(filename):
    timestamp_dir = datetime.now().strftime('%Y%m%d')
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], timestamp_dir)
    os.makedirs(upload_dir, exist_ok=True)
    
    base_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    timestamp = datetime.now().strftime('%H%M%S')
    unique_filename = f"{base_name}_{timestamp}{extension}"
    
    return os.path.join(upload_dir, unique_filename)


@app.route('/')
def index():
    metadata = get_metadata()
    has_documents = len(metadata.get('documents', [])) > 0
    version = get_version()
    config = load_config()
    return render_template('index.html', 
                         has_documents=has_documents, 
                         metadata=metadata,
                         version=version,
                         config=config)


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    sort_by = data.get('sort_by', 'relevance')
    
    if not query:
        return jsonify({'results': [], 'query': query})
    
    config = load_config()
    num_results = config.get('num_search_results', 5)
    
    results = search_in_index(query, num_matches=num_results, sort_by=sort_by)
    return jsonify({'results': results, 'query': query})


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    uploaded_files = []
    errors = []
    
    for file in files:
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)
            filepath = get_upload_path(original_filename)
            file.save(filepath)
            
            success, message, doc_id = add_document_to_index(filepath, original_filename, original_filename)
            if success:
                uploaded_files.append(original_filename)
            else:
                errors.append(f"{original_filename}: {message}")
                if os.path.exists(filepath):
                    os.remove(filepath)
        else:
            errors.append(f"{file.filename}: Invalid file type. Only PDF, DOCX, and TXT allowed.")
    
    metadata = get_metadata()
    
    response = {
        'success': len(uploaded_files) > 0,
        'uploaded': uploaded_files,
        'errors': errors,
        'metadata': metadata
    }
    
    return jsonify(response)


@app.route('/documents', methods=['GET'])
def list_documents():
    metadata = get_metadata()
    return jsonify(metadata)


@app.route('/documents/<doc_id>', methods=['GET'])
def view_document(doc_id):
    doc_content = get_document_content(doc_id)
    if doc_content:
        return jsonify(doc_content)
    return jsonify({'error': 'Document not found'}), 404


@app.route('/documents/<doc_id>', methods=['DELETE'])
def delete_doc(doc_id):
    success, message = delete_document(doc_id)
    if success:
        metadata = get_metadata()
        return jsonify({'success': True, 'message': message, 'metadata': metadata})
    return jsonify({'success': False, 'error': message}), 404


@app.route('/config', methods=['GET'])
def get_config():
    config = load_config()
    return jsonify(config)


@app.route('/config', methods=['POST'])
def update_config():
    data = request.get_json()
    
    current_config = load_config()
    current_model = current_config.get('model_repo_id')
    
    # Update config
    for key in ['model_repo_id', 'chunk_size', 'chunk_overlap', 'num_search_results', 'top_k', 'dimension']:
        if key in data:
            current_config[key] = data[key]
    
    save_config(current_config)
    
    # If model changed, offer to rebuild index
    new_model = current_config.get('model_repo_id')
    needs_rebuild = (current_model != new_model) or \
                   (data.get('chunk_size') and data.get('chunk_size') != current_config.get('chunk_size')) or \
                   (data.get('chunk_overlap') and data.get('chunk_overlap') != current_config.get('chunk_overlap'))
    
    return jsonify({
        'success': True,
        'config': current_config,
        'needs_rebuild': needs_rebuild
    })


@app.route('/rebuild-index', methods=['POST'])
def rebuild_index():
    try:
        success, message = rebuild_index_with_new_config()
        if success:
            metadata = get_metadata()
            return jsonify({
                'success': True,
                'message': message,
                'metadata': metadata
            })
        else:
            return jsonify({'success': False, 'error': message}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/metadata', methods=['GET'])
def metadata():
    return jsonify(get_metadata())


if __name__ == '__main__':
    app.run(debug=True)

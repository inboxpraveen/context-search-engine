import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from document_processor import (
    add_document_to_index, 
    search_in_index, 
    get_metadata,
    delete_document,
    get_document_content
)

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
    return render_template('index.html', has_documents=has_documents, metadata=metadata)


@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query = data.get('query', '').strip()
    
    if not query:
        return jsonify({'results': [], 'query': query})
    
    results = search_in_index(query, num_matches=3)
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


@app.route('/metadata', methods=['GET'])
def metadata():
    return jsonify(get_metadata())


if __name__ == '__main__':
    app.run(debug=True)

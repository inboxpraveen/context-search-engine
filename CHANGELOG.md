# Changelog

All notable changes to the Context Search Engine project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-01

### Added
- **Google-Style Search Interface**: Complete UI redesign with centered search box and cleaner layout
- **Configuration System**: Users can now configure:
  - HuggingFace model repository ID for custom embedding models
  - Chunk window size (words per chunk)
  - Chunk overlap size
  - Number of search results to display
  - Top K parameter for search pool
  - Embedding dimension
- **Enhanced Search Results**: Results now include:
  - Document name
  - Page number (for PDFs)
  - Chunk number
  - "View Source" button to see full document
- **Sort and Filter**: Search results can be sorted by:
  - Relevance (default)
  - Recent documents first
- **Top Navigation Bar**: Quick access buttons for:
  - Upload Documents
  - Configuration settings
- **Page Number Tracking**: PDFs now track and display page numbers for each chunk
- **Dynamic Model Loading**: Support for any HuggingFace sentence-transformer compatible model
- **Index Rebuilding**: Automatic detection when configuration changes require index rebuild
- **Version Display**: Application version now shown in bottom left of UI

### Changed
- **UI/UX Complete Redesign**: Moved from card-based to Google search-style interface
- **Search Behavior**: Type-ahead search now activates after 3 characters with 500ms debounce
- **Result Display**: Enhanced result cards with better metadata visibility
- **Configuration Storage**: Settings now persist in `app_config.json`
- **Modal System**: Unified modal for all popups (upload, config, documents, etc.)

### Improved
- Better document organization with timestamp-based folder structure
- More detailed document metadata tracking
- Cleaner, more intuitive navigation
- Responsive design improvements for mobile devices
- Performance optimizations for search

### Technical
- Added `config.py` for centralized configuration management
- Updated `document_processor.py` with:
  - AutoTokenizer and AutoModel support for custom models
  - Page number extraction for PDFs
  - Configurable chunking parameters
  - Model caching for better performance
- Enhanced Flask endpoints:
  - `/config` GET/POST for configuration management
  - `/rebuild-index` POST for reindexing with new settings
- Complete rewrite of CSS for modern, minimalist design

---

## [1.0.0] - 2025-11-15

### Initial Release

#### Features
- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Drag & Drop Interface**: Easy file upload with drag and drop
- **Semantic Search**: DistilBERT-based vector search using FAISS
- **Document Management**:
  - View all uploaded documents
  - View document content
  - Delete documents with confirmation
- **Auto-indexing**: Automatic text extraction and vectorization
- **Responsive Design**: Mobile-friendly glassmorphism UI
- **Real-time Search**: Search as you type functionality
- **Document Stats**: Dashboard showing document and chunk counts
- **Toast Notifications**: User-friendly feedback system

#### Technical Stack
- Flask web framework
- DistilBERT for text embeddings
- FAISS for vector similarity search
- PyPDF2 for PDF processing
- python-docx for Word document processing
- Modern vanilla JavaScript (no frameworks)
- CSS3 with glassmorphism effects

#### Architecture
- Client-side: HTML5, CSS3, JavaScript
- Server-side: Python Flask
- ML: Transformers (HuggingFace)
- Vector DB: FAISS (Facebook AI)
- Storage: Local filesystem with pickle serialization

---

## Release Notes

### Version 2.0.0 Highlights

This major release transforms the application into a fully configurable semantic search platform. The new Google-style interface makes it feel like a professional product rather than a learning tool, while maintaining its educational value.

**Key Improvements:**
- 🎨 **Professional UI**: Clean, minimalist design inspired by Google Search
- ⚙️ **Full Configurability**: Swap models, adjust chunking, and tune search parameters
- 📊 **Better Results**: Enhanced metadata including page numbers and chunk locations
- 🔄 **Flexible Sorting**: Sort by relevance or recency
- 🚀 **Performance**: Model caching and optimized search

**Migration from 1.x:**
If upgrading from version 1.x, your existing documents will work with version 2.0. However, to take advantage of new features like page numbers and custom models, you may want to reindex your documents using the "Configure" menu.

### Version 1.0.0 Highlights

The initial release provided a solid foundation for semantic document search with an intuitive interface and core functionality. It demonstrated the power of transformer-based embeddings for understanding document context beyond keyword matching.

---

## Future Roadmap

### Planned for v2.1.0
- [ ] Multi-user support with authentication
- [ ] Document folders/categories
- [ ] Search history tracking
- [ ] Export search results

### Planned for v2.2.0
- [ ] Batch folder upload
- [ ] Advanced filters (date range, document type)
- [ ] Highlighting of matched text in results
- [ ] Query suggestions

### Planned for v3.0.0
- [ ] RESTful API
- [ ] Docker containerization
- [ ] Cloud deployment templates
- [ ] Analytics dashboard
- [ ] Multilingual support

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for information on how to contribute to this changelog and the project.


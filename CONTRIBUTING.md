# Contributing to Context Search Engine

Thank you for your interest in contributing to the Context Search Engine! This project is a learning tool and experimentation platform for semantic search, and we welcome contributions from everyone—whether you're fixing a typo, adding a feature, or improving documentation.

## 🌟 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Documentation](#documentation)
- [Community](#community)

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- Be respectful and professional
- Accept constructive criticism gracefully
- Focus on what's best for the project and community
- Show empathy towards other contributors
- Use welcoming and inclusive language

### Our Standards

**Encouraged behavior:**
- Demonstrating empathy and kindness
- Being respectful of differing viewpoints
- Giving and accepting constructive feedback
- Taking responsibility and apologizing for mistakes
- Focusing on what's best for the community

**Unacceptable behavior:**
- Trolling, insulting, or derogatory comments
- Public or private harassment
- Publishing others' private information
- Any conduct inappropriate in a professional setting

## 🤝 Ways to Contribute

There are many ways you can contribute to this project:

### 🐛 Bug Fixes
- Found a bug? Fix it! Check existing issues first to avoid duplication
- Test edge cases and document them
- Add unit tests for your bug fix

### ✨ New Features
- Implement features from the [roadmap](README.md#-whats-next)
- Propose and implement your own ideas
- Ensure features align with project goals (learning, research, experimentation)

### 📚 Documentation
- Improve README, CHANGELOG, or this guide
- Add code comments for complex logic
- Create tutorials or Jupyter notebooks
- Write blog posts or create video tutorials
- Add inline documentation for functions and classes

### 🎨 UI/UX Improvements
- Enhance the interface design
- Improve accessibility (ARIA labels, keyboard navigation)
- Add themes or customization options
- Optimize responsive design for different devices
- Create new visualizations for search results

### 🧪 Testing
- Write unit tests for existing code
- Add integration tests for API endpoints
- Perform performance testing and benchmarking
- Test with different document types and sizes
- Test different embedding models

### 🌍 Localization
- Translate the UI to other languages
- Ensure text is internationalization-ready
- Add language-specific documentation

### 📊 Examples & Tutorials
- Create example use cases
- Build sample datasets for testing
- Write Jupyter notebook tutorials
- Record video walkthroughs
- Share A/B testing experiments

### 🔧 DevOps & Tools
- Improve development scripts
- Create Docker configurations
- Set up CI/CD pipelines
- Add deployment templates (AWS, GCP, Azure)
- Create development environment guides

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.8 or higher
- **pip**: Latest version
- **Git**: For version control
- **Text Editor/IDE**: VS Code, PyCharm, or your preference
- **RAM**: 4GB minimum (8GB recommended)
- **Internet**: First run downloads ~250MB of model weights

### Setting Up Your Development Environment

1. **Fork the repository**
   
   Click the "Fork" button on GitHub to create your own copy.

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/context-search-engine.git
   cd context-search-engine
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/inboxpraveen/context-search-engine.git
   ```

4. **Create a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Verify installation**
   ```bash
   python app.py
   ```
   Navigate to `http://localhost:5000` to see if it works.

### Understanding the Project Structure

```
context-search-engine/
│
├── app.py                      # Flask application & API endpoints
├── document_processor.py       # Core logic: embedding, indexing, search
├── config.py                   # Configuration management
├── search_engine.py           # Legacy (can be removed)
├── create_index.py            # Legacy (can be removed)
│
├── templates/
│   └── index.html             # Main UI (single-page application)
│
├── static/
│   ├── css/
│   │   └── style.css          # Application styling
│   └── images/                # UI assets & screenshots
│
├── uploads/                   # User-uploaded documents
│   └── YYYYMMDD/             # Auto-organized by date
│
├── faiss_index.idx            # FAISS vector index (generated)
├── index_to_chunk.pkl         # Index to chunk mapping (generated)
├── document_metadata.pkl      # Document metadata (generated)
├── app_config.json           # User configuration (generated)
│
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore rules
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # This file
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

### Key Components

**app.py**
- Flask web server
- API endpoints (`/search`, `/upload`, `/config`, etc.)
- Request/response handling
- File upload management

**document_processor.py**
- Text extraction (PDF, DOCX, TXT)
- Document chunking with configurable overlap
- Embedding generation using HuggingFace models
- FAISS index management
- Search functionality with sorting
- Document deletion and index rebuilding

**config.py**
- Configuration loading and saving
- Default settings
- Version management

**templates/index.html**
- Single-page application UI
- Search interface
- Document upload modal
- Configuration modal
- Document management interface
- Client-side JavaScript for interactivity

**static/css/style.css**
- Modern, minimalist design
- Google-style search interface
- Responsive layout
- Modal styling

## 🔄 Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your changes:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Branch Naming Conventions

- `feature/` - New features (e.g., `feature/multi-user-support`)
- `fix/` - Bug fixes (e.g., `fix/search-crash-empty-query`)
- `docs/` - Documentation changes (e.g., `docs/update-readme`)
- `refactor/` - Code refactoring (e.g., `refactor/simplify-chunking`)
- `test/` - Adding tests (e.g., `test/add-search-tests`)
- `chore/` - Maintenance tasks (e.g., `chore/update-dependencies`)

### 2. Make Your Changes

- Write clean, readable code
- Follow the code style guidelines (see below)
- Add comments for complex logic
- Keep changes focused—one feature/fix per PR
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run the application
python app.py

# Test manually:
# - Upload different file types (PDF, DOCX, TXT)
# - Perform searches with various queries
# - Test configuration changes
# - Test document deletion
# - Verify responsive design on mobile
# - Check browser console for errors
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add multi-language support for UI"
```

See [Commit Message Guidelines](#commit-message-guidelines) for details.

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

- Go to your fork on GitHub
- Click "New Pull Request"
- Select your feature branch
- Fill out the PR template (see below)
- Submit the PR

## 📝 Code Style Guidelines

### Python (Backend)

We follow **PEP 8** style guide:

- **Indentation**: 4 spaces (no tabs)
- **Line length**: 100 characters maximum (preferably 80)
- **Imports**: Grouped (standard library, third-party, local)
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
- **Docstrings**: Use for all functions, classes, and modules

**Example:**

```python
def extract_text_from_pdf(file_path):
    """
    Extract text from PDF with page tracking.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        list: List of dicts with page_number and text
    """
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
```

**Best Practices:**
- Use type hints where appropriate
- Handle exceptions gracefully
- Avoid global variables (use caching patterns instead)
- Keep functions focused on a single task
- Use list comprehensions for simple iterations
- Prefer f-strings for string formatting

### JavaScript (Frontend)

Use **ES6+ features**:

- **Indentation**: 2 spaces
- **Variables**: `const` and `let` (never `var`)
- **Naming**:
  - `camelCase` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
- **Semicolons**: Use them consistently
- **Quotes**: Single quotes for strings (unless template literals)

**Example:**

```javascript
const searchDocuments = async (query, sortBy = 'relevance') => {
  try {
    const response = await fetch('/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, sort_by: sortBy })
    });
    const data = await response.json();
    return data.results;
  } catch (error) {
    console.error('Search failed:', error);
    showToast('Search failed. Please try again.', 'error');
    return [];
  }
};
```

**Best Practices:**
- Use async/await for asynchronous operations
- Handle errors with try/catch
- Use arrow functions for callbacks
- Prefer template literals for multi-line strings
- Use destructuring for cleaner code
- Add JSDoc comments for complex functions

### HTML

Use **semantic HTML5**:

- Proper indentation (2 spaces)
- Semantic tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`)
- Accessibility attributes (ARIA labels, alt text)
- Valid HTML (no unclosed tags)

**Example:**

```html
<main role="main" class="search-container">
  <header class="search-header">
    <h1>Context Search Engine</h1>
  </header>
  
  <section class="search-box-container">
    <input 
      type="text" 
      id="searchQuery" 
      placeholder="Search your documents..."
      aria-label="Search query input"
      autocomplete="off"
    />
  </section>
</main>
```

### CSS

Use **BEM naming convention** (preferred) or consistent class naming:

- **Indentation**: 2 spaces
- **Naming**: Descriptive class names
- **Organization**: Group related rules
- **Comments**: Explain complex layouts or hacks

**Example:**

```css
/* Search Container */
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.search-container__header {
  text-align: center;
  margin-bottom: 2rem;
}

.search-container__input {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-container__input:focus {
  outline: none;
  border-color: #4285f4;
  box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.1);
}
```

### Comments

Write comments that explain **WHY**, not **WHAT**:

**Bad:**
```python
# Set chunk size to 500
chunk_size = 500
```

**Good:**
```python
# Default chunk size balances context preservation with search precision
# Smaller chunks = more precise search, less context
# Larger chunks = more context, less precise search
chunk_size = 500
```

**When to comment:**
- Complex algorithms or logic
- Non-obvious design decisions
- Performance optimizations
- Workarounds for known issues
- TODOs for future improvements

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting a PR, test the following:

**Upload Functionality:**
- [ ] Upload PDF file
- [ ] Upload DOCX file
- [ ] Upload TXT file
- [ ] Upload multiple files at once
- [ ] Drag and drop files
- [ ] Try invalid file types (should reject)
- [ ] Try empty files (should handle gracefully)

**Search Functionality:**
- [ ] Search with 1-2 characters (should not trigger)
- [ ] Search with 3+ characters (should trigger after 500ms)
- [ ] Search with empty query
- [ ] Search with special characters
- [ ] Sort by relevance
- [ ] Sort by recent
- [ ] View search results
- [ ] Click "View Source" button

**Configuration:**
- [ ] Change model (verify rebuild prompt)
- [ ] Change chunk size (verify rebuild prompt)
- [ ] Change chunk overlap
- [ ] Change search results count
- [ ] Change top K parameter
- [ ] Change dimension
- [ ] Save configuration
- [ ] Rebuild index

**Document Management:**
- [ ] View all documents
- [ ] View document content
- [ ] Delete document (verify confirmation)
- [ ] Delete last document (verify empty state)

**UI/UX:**
- [ ] Responsive on mobile (< 768px)
- [ ] Responsive on tablet (768px - 1024px)
- [ ] Responsive on desktop (> 1024px)
- [ ] Dark/light mode compatibility (if implemented)
- [ ] All modals open and close correctly
- [ ] Toast notifications appear and disappear
- [ ] No console errors in browser

**Edge Cases:**
- [ ] No documents uploaded (empty state)
- [ ] Large files (> 10MB)
- [ ] Documents with no text
- [ ] Very long queries (> 512 tokens)
- [ ] Network errors (disconnect during upload)

### Writing Unit Tests (Future)

Currently, the project doesn't have automated tests, but contributions to add them are welcome!

**Testing framework suggestions:**
- **Backend**: `pytest` for Python
- **Frontend**: `Jest` or `Mocha` for JavaScript

**Example test structure:**

```python
# tests/test_document_processor.py
import pytest
from document_processor import chunk_text, extract_text_from_pdf

def test_chunk_text_basic():
    text = "word " * 1000  # 1000 words
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 0
    assert all(len(chunk.split()) <= 100 for chunk in chunks)

def test_chunk_text_with_overlap():
    text = "word " * 200
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    # Verify overlap between consecutive chunks
    assert len(chunks) >= 2
```

## 📨 Commit Message Guidelines

We follow **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring (no feature change or bug fix)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `ci`: CI/CD changes

### Examples

```bash
# Simple feature
git commit -m "feat: add support for markdown file upload"

# Bug fix with scope
git commit -m "fix(search): handle empty query gracefully"

# Documentation
git commit -m "docs: update installation instructions in README"

# With body and footer
git commit -m "feat: add user authentication

- Add login/logout endpoints
- Implement JWT token-based auth
- Add user session management
- Update UI with login form

Closes #123"
```

### Best Practices

- Use imperative mood ("add" not "added")
- Keep subject line under 72 characters
- Capitalize first letter of subject
- No period at the end of subject
- Separate subject from body with blank line
- Use body to explain what and why, not how
- Reference issues and PRs in footer

## 🔀 Pull Request Process

### Before Submitting

1. **Update your branch** with latest upstream changes:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Review your changes**:
   ```bash
   git diff main...your-feature-branch
   ```

3. **Ensure all tests pass** (manual testing checklist)

4. **Update documentation** if needed:
   - README.md for user-facing changes
   - CHANGELOG.md for version history
   - Code comments for complex logic

### PR Template

Use this template when creating a PR:

```markdown
## Description

Brief description of what this PR does.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Related Issue

Fixes #(issue number)
Closes #(issue number)

## Changes Made

- Change 1
- Change 2
- Change 3

## Screenshots (if applicable)

Add screenshots for UI changes.

## Testing Done

Describe the testing you performed:
- [ ] Tested with PDF files
- [ ] Tested with DOCX files
- [ ] Tested on mobile devices
- [ ] Checked browser console for errors
- [ ] etc.

## Checklist

- [ ] My code follows the project's code style
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] I have tested my changes thoroughly
- [ ] I have updated the CHANGELOG.md (for significant changes)

## Additional Notes

Any additional information, concerns, or questions.
```

### Review Process

1. **Automated checks** (if configured):
   - Code style checks
   - Tests (when implemented)
   - Build verification

2. **Manual review** by maintainers:
   - Code quality and style
   - Functionality correctness
   - Documentation completeness
   - Test coverage

3. **Feedback and iteration**:
   - Address reviewer comments
   - Make requested changes
   - Push updates to your branch

4. **Approval and merge**:
   - Requires approval from at least one maintainer
   - Squash and merge (or rebase) into main
   - PR will be closed automatically

## 🐛 Reporting Issues

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to the latest version** to see if issue persists
3. **Try to reproduce** the issue consistently

### Issue Template

Use this template when reporting bugs:

```markdown
## Bug Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. Upload '...'
4. See error

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Screenshots

If applicable, add screenshots to help explain your problem.

## Environment

- OS: [e.g., Windows 10, macOS 12.6, Ubuntu 22.04]
- Python Version: [e.g., 3.9.7]
- Browser: [e.g., Chrome 108, Firefox 107]
- Application Version: [e.g., 2.0.0]

## Additional Context

Add any other context about the problem here.

## Possible Solution (optional)

If you have an idea of how to fix it, share it here.
```

### Issue Labels

We use these labels to categorize issues:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention needed
- `question` - Further information requested
- `wontfix` - This will not be worked on
- `duplicate` - This issue already exists
- `invalid` - This doesn't seem right

## 💡 Feature Requests

### Proposing Features

We welcome feature proposals! Here's how to propose one:

1. **Check the roadmap** in README.md to see if it's already planned
2. **Search existing issues** to avoid duplicates
3. **Create a new issue** with the `enhancement` label

### Feature Request Template

```markdown
## Feature Description

A clear and concise description of the feature.

## Problem It Solves

Explain what problem this feature would solve or what need it addresses.

## Proposed Solution

Describe how you envision this feature working.

## Alternative Solutions

Describe any alternative solutions or features you've considered.

## Use Cases

Provide concrete examples of when/how this feature would be used:

1. As a [user type], I want [goal] so that [benefit]
2. Example scenario 2
3. Example scenario 3

## Mockups/Examples (optional)

If you have mockups, wireframes, or examples from other projects, share them here.

## Additional Context

Add any other context or screenshots about the feature request.

## Are you willing to implement this?

- [ ] Yes, I can submit a PR
- [ ] I can help with testing
- [ ] I can help with documentation
- [ ] I need someone else to implement it
```

## 📖 Documentation

### Types of Documentation

**Code Documentation:**
- Inline comments for complex logic
- Docstrings for all functions and classes
- Type hints for function parameters

**User Documentation:**
- README.md - Main project documentation
- CHANGELOG.md - Version history and changes
- CONTRIBUTING.md - This file

**Educational Content:**
- Jupyter notebooks with examples
- Tutorial blog posts
- Video walkthroughs
- Use case demonstrations

### Documentation Style

- Use clear, simple language
- Provide code examples
- Include screenshots for UI features
- Link to related resources
- Keep it up to date

### Updating Changelog

When making significant changes, update CHANGELOG.md:

```markdown
## [Unreleased]

### Added
- New feature description

### Changed
- What was changed

### Fixed
- Bug fix description

### Removed
- What was removed
```

## 🌐 Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion (if enabled)
- **Email**: [inboxpraveen.17@gmail.com](mailto:inboxpraveen.17@gmail.com)

### Staying Updated

- **Watch** the repository for notifications
- **Star** ⭐ if you find it useful
- **Fork** to experiment and contribute
- **Share** with others who might benefit

### Recognition

Contributors will be:
- Listed in future releases
- Mentioned in CHANGELOG for significant contributions
- Credited in documentation and README (planned)

## 🎓 Learning Resources

### Project Technologies

**Vector Embeddings & Transformers:**
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [The Illustrated BERT](https://jalammar.github.io/illustrated-bert/)
- [Understanding DistilBERT](https://medium.com/huggingface/distilbert-8cf3380435b5)

**FAISS:**
- [FAISS Documentation](https://faiss.ai/)
- [FAISS Tutorial by Pinecone](https://www.pinecone.io/learn/faiss-tutorial/)

**Semantic Search:**
- [What is Semantic Search?](https://www.elastic.co/what-is/semantic-search)
- [Building a Semantic Search Engine](https://www.pinecone.io/learn/semantic-search/)

**Web Development:**
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [MDN Web Docs](https://developer.mozilla.org/)

### Development Skills

**Python Best Practices:**
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Real Python Tutorials](https://realpython.com/)
- [Python Documentation](https://docs.python.org/3/)

**Git & GitHub:**
- [GitHub Docs](https://docs.github.com/)
- [Pro Git Book](https://git-scm.com/book/en/v2)
- [Oh Shit, Git!?!](https://ohshitgit.com/)

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

The MIT License allows commercial use, modification, distribution, and private use. See the [LICENSE](LICENSE) file for details.

## 🙏 Thank You!

Thank you for taking the time to contribute to Context Search Engine! Every contribution, no matter how small, makes a difference.

Whether you're fixing a typo, reporting a bug, suggesting a feature, or writing code—you're helping make this project better for everyone who wants to learn about and experiment with semantic search.

Happy coding! 🚀

---

**Questions?** Feel free to open an issue or reach out via email at [inboxpraveen.17@gmail.com](mailto:inboxpraveen.17@gmail.com).

**Want to contribute but not sure where to start?** Look for issues labeled `good first issue` or `help wanted`!


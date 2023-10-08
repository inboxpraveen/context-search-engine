from flask import Flask, render_template, request

from search_engine import search_in_index


# Initialize the Flask application
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """
    Serve the main landing page.
    
    This endpoint is responsible for rendering the main HTML template.
    
    Methods:
    - GET: Returns the main landing page.
    
    Returns:
    - HTML template: Renders 'index.html'.
    
    Example:
    Visit the application root, e.g., http://localhost:5000/
    """
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    """
    Conduct a search based on the user's query and return the results.
    
    This endpoint takes a user query from the form, searches the FAISS index
    (or any other search mechanism defined in the 'search_in_index' function), 
    and returns the matched results.
    
    Methods:
    - POST: Accepts the search query, processes it, and returns the results.
    
    Returns:
    - HTML template: Renders 'index.html' with the search results.
    
    Example:
    POST to http://localhost:5000/search with form data containing a 'query'.
    """
    query = request.form['query']  # Extracting the query from the form
    result = search_in_index(query)  # Searching the index for the query
    return render_template('index.html', result=result)


if __name__ == '__main__':
    """
    Start the Flask development server.
    
    The server will be in debug mode, meaning changes to files 
    will auto-reload the application and any errors will be displayed in detail.
    """
    app.run(debug=True)

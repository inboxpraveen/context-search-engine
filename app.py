from flask import Flask, render_template, request
from search_engine import search_in_index

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    result = search_in_index(query)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

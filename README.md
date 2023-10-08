# Contextual Text Search Engine Using Vector Data and FAISS

The primary objective of this project is to provide a user-friendly interface that enables users to perform contextual searches across a corpus of text documents. By leveraging the power of Hugging Face's Distil BERT and Facebook's FAISS, we aim to return highly relevant text passages based on the semantic meaning of the user's query rather than mere keyword matches. This project serves as a starting point for developers, researchers, and enthusiasts who wish to dive deeper into the world of contextualized text search and enhance their applications with state-of-the-art NLP techniques.



## 1. Prerequisites

You can install the all the necessary packages via pip using requirements files:

```shell
pip install -r requirements.txt
```

However, if you have a GPU, you are requested to install FAISS GPU for faster and larger database integrations.



## 2. Scope of the Project

The current version of this project encompasses:

- A basic web interface built using Flask where users can input and submit their search queries.
- A backend search engine that:
  - Transforms user queries into semantic vectors using DistilBERT.
  - Efficiently compares the query vector against a pre-indexed set of vectors (corresponding to text documents) stored in a FAISS index.
  - Returns the most contextually relevant text passage from the corpus.
  - Highlights the keywords in the returned text passage that are contextually matched.

While the project offers a functional contextual search system, it is designed to be modular, allowing for potential expansion and integration into larger systems or applications.



## 3. Explanation of Overall Approach

The foundation of this project lies in the belief that modern NLP techniques can offer far more accurate and contextually relevant search results compared to traditional keyword-based methods. Here's a breakdown of our approach:

1. **User Interface**: The frontend, built using Flask, serves as the interaction point for the users. It's kept simple and intuitive.
2. **Query Vectorization**: When a user submits a query, the backend system transforms it into a semantic vector using Distil BERT. This vector encapsulates the meaning of the query.
3. **Searching with FAISS**: FAISS, an efficient similarity search library, is utilized to quickly compare the query vector against a pre-established index of vectors from the text corpus. The closest match, in terms of semantic meaning, is identified.
4. **Returning Results**: Once the most relevant text passage is identified, the system also highlights keywords or phrases that match the user's query contextually, offering a visual cue to the user about why a particular passage was deemed relevant.
5. **Iterative Refinement**: The underlying models and techniques are open to refinements based on newer research, user feedback, and specific application needs.



## 4. Project Structure

1. `index.html`: Front-end HTML page for inputting search queries.
2. `app.py`: Flask application that serves the front-end and handles search queries.
3. `search_engine.py`: Contains logic for embedding generation, FAISS searching, and keyword highlighting.

```
/context_search/
    - templates/
        - index.html
    - app.py
    - search_engine.py
    - index_to_chunk.pkl
    - faiss_index.idx
```



## 5. Usage

1. Ensure you have a trained FAISS index (`faiss_index.idx`) and an accompanying mapping from index to text chunk (`index_to_chunk.pkl`).
2. Start the Flask application:

```
flask run
```

1. Open a web browser and go to `http://localhost:5000`.
2. Enter a search query and observe the contextually relevant result.



## 6. Things to Do - for Improvements

There's always room for enhancements. Here are some potential improvements and additional features that can be integrated:

1. **Scalability**: Currently, the system is built for relatively smaller corpora. Consider leveraging distributed systems or cloud-based solutions to handle larger datasets.
2. **Advanced Highlighting**: Improve the keyword highlighting system to ensure that contextually relevant phrases (and not just individual words) are highlighted.
3. **Feedback Loop**: Incorporate a user feedback mechanism where users can rate the relevance of the returned results. This can be used for fine-tuning the models in the future.
4. **Support for Multiple Document Types**: Extend support for various document types such as PDF, DOCX, etc., allowing users to search across different formats.
5. **Enhanced Frontend**: Improve the user interface, perhaps integrating advanced features like autocomplete, query suggestions, or a more sophisticated result display.
6. **Support for Multilingual Searches**: Expand the system to support queries in multiple languages, returning results from a multilingual corpus.



## License

This project is under the MIT License. Feel free to use, modify, distribute, and contribute.

## Contributing

If you're interested in improving this project or adding new features, your contributions are welcome! Please open a Pull Request or Issue on this repository.


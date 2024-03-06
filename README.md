# LibrarySearch
Simple Semantic Search Application to search books by context.

# Initial Setup

You may need to run the following for the env setup

pip install sentence-transformers
pip install chromaDB


# Embedding Pipeline (Preprocessing)

generate_embeddings.py - Used as the one-time processor to generate the embeddings for the given of books. Place chapter wise content for each book in separate folder under books/ folder. Each book folder should adhere to the following,

- Each chapter contents in seaparate text file named as <chapter-num>.txt
- A metadata.json file should be present with title and author name.

Note the samples in here are obtained from https://storage.cloud.google.com/sfr-books-dataset-chapters-research/all_chapterized_books.zip

Run below command to generate the embeddings and store in chroma db:

python .\generate_embeddings.py

# Start Application

- Run app.py
- URL to access the application will be in the terminal logs.

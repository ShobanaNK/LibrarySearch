import numpy as np
import pandas as pd
import os
import re
import json
import copy
import ast
from sentence_transformers import SentenceTransformer
import chromadb

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "library_collection"
embedder = SentenceTransformer(MODEL_NAME)
chroma_client = chromadb.PersistentClient()

def get_text(filename):
    fh = open(filename)
    return fh.read()

# Function to generate embeddings for text
def generate_embeddings(texts):
    embeddings = embedder.encode(texts, convert_to_tensor=True)
    return embeddings.tolist()

def Merge(dict1, dict2):
    dict1.update(dict2)
    return dict1

# Read the chapter wise content for a book in a given directory and builds the embeddings & metadata to be stored in chroma-db
# chapter contents are expected to be in <chapter-num.txt> format
def generate_data(folder):
    result_df = pd.DataFrame()
    
    result_df['chapter_files'] = [f for f in os.listdir(folder) if re.match(r'[0-9]+\.txt', f)]
    print('processing {} with {} files'.format(folder, len(result_df['chapter_files'])))
    
    # Opening metdata JSON file and convert to dict
    mdf = open('{}/metadata.json'.format(folder))
    metadata = json.loads(mdf.read())
    
    result_df['Document'] = result_df['chapter_files'].apply(lambda x: get_text('{0}/{1}'.format(folder, x)))
    result_df['Embedding'] = result_df['Document'].apply(lambda x: generate_embeddings(x))
    result_df['Id'] = result_df['chapter_files'].apply(lambda x: str(re.search('/([0-9]+)-chapters', folder)[1]) + '-' + str(x.split('.')[0]))
    result_df['Metadata'] = result_df['chapter_files'].apply(lambda x: Merge({'chapter': x.split('.')[0]}, metadata))

    print('returing {} results'.format(len(result_df)))
    return result_df
    

def update_ChromaCollection(data):
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

    # Add the documents, embeddings, and ids into the collection
    book_collection = collection.add(
        embeddings = data['Embedding'].to_list(),
        documents = data['Document'].to_list(),
        metadatas = data['Metadata'].to_list(),
        ids = data['Id'].to_list(),
    )

    return book_collection

# returns the book details containing matching query data
def query_collection(query):
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    # Query the ChromaDB collection using `collection.query()
    results = collection.query(
        query_texts=query, # Here we are passing the texts for search. Probably makes sense to pass the query_embeddings https://docs.trychroma.com/reference/py-collection#query
        n_results=3,
        include = ['metadatas', 'distances']
    )

    return "</br> ".join([ "Chapter " + x['chapter'] + " in " + x['title'] + " writen by " + x["author"] for x in results["metadatas"][0]])

from sentence_transformers import SentenceTransformer
import numpy as np
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

# Read the cleaned text file
cleaned_text_file_path = '/Users/sanchay/Documents/cleaned_diabetes_text .txt'
with open(cleaned_text_file_path, 'r') as file:
    cleaned_text = file.read()

# simple split by period.
sentences = cleaned_text.split('. ')

# Encode the text into vectors
text_embeddings = model.encode(sentences)

embeddings_file_path = '/Users/sanchay/Documents/vectorized_diabetes_data.json'
with open(embeddings_file_path, 'w') as embeddings_file:
    # Convert numpy arrays to lists for JSON serialization
    embeddings_list = [embedding.tolist() for embedding in text_embeddings]
    json.dump(embeddings_list, embeddings_file)

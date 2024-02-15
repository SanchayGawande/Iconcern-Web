from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('/Users/sanchay/Documents/cleaned_diabetes_text .txt', 'r') as file:
    cleaned_text = file.read()


text_embeddings = model.encode([cleaned_text]) 
from sentence_transformers import SentenceTransformer
import pickle

# Initialize the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Define your list of sentences
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "Innovation distinguishes between a leader and a follower.",
    "To be or not to be, that is the question.",
    "The best way to predict the future is to invent it.",
    "Data is a precious thing and will last longer than the systems themselves.",
    "A person who never made a mistake never tried anything new.",
    "The only way to do great work is to love what you do."
]

# Generate embeddings for each sentence
embeddings = model.encode(sentences)

# Save embeddings to a file
with open('sentence_embeddings.pkl', 'wb') as f:
    pickle.dump(embeddings, f)

# To load the embeddings back into memory
with open('sentence_embeddings.pkl', 'rb') as f:
    loaded_embeddings = pickle.load(f)

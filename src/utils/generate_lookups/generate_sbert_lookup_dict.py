"""
This script represents the controlled vocabulary terms as embeddings and saves them to a lookup dictionary.
The Sentence-BERT model is used. 

Input: a ttl file with controlled vocabulary terms
Output: a lookup dictionary with terms as keys and embeddings as values, saved as a .pkl file

"""


# Import libraries
import rdflib
#from utils.helpers import get_fasttext_vec
import logging
from sentence_transformers import SentenceTransformer
import numpy as np


def get_sbert_embedding(text: str) -> np.ndarray:
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding  # returns a NumPy array




# Load model 
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
logging.info(f"Using Sentence-BERT model: {model}")

# Read the turtle file 
path = "../../data/aatc.ttl"

g = rdflib.Graph()
g.parse(path, format="turtle")


# create lookup dictionary for AATC concepts
aatc_lookup = {}
for s, p, o in g:
    if p.endswith("prefLabel"):
        if o.language == "en":
            #aatc_lookup[str(o)] = str(s)
            # add embedding 
            vec = get_sbert_embedding(str(o))
            aatc_lookup[str(o)] = vec

# print first 5 items
for i, (term, emb) in enumerate(aatc_lookup.items()):
    if i < 5:
        print(f"Term: {term} | Embedding shape: {emb.shape}")
    else:
        break

print(f"~ {len(aatc_lookup)} AATC terms represented as embeddings ~")

# Save the lookup dictionary
import pickle
with open("data/aatc_sbert_lookup.pkl", "wb") as f:
    pickle.dump(aatc_lookup, f)
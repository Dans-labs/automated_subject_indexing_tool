"""
This script represents the controlled vocabulary terms as embeddings and saves them to a lookup dictionary.
The FastText model is used. 

Input: a ttl file with controlled vocabulary terms
Output: a lookup dictionary with terms as keys and embeddings as values, saved as a .pkl file

"""




# Import libraries
import rdflib
#from utils.helpers import get_fasttext_vec
import logging
import fasttext



model_path = "models/cc.en.300.bin"
logging.info(f"Using FastText model at: {model_path}")
ft = fasttext.load_model(model_path)


def get_fasttext_vec(word: str):
    return ft.get_word_vector(word)   # returns a NumPy array (300,)


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
            vec = get_fasttext_vec(str(o))
            aatc_lookup[str(o)] = vec

# print first 5 items
for i, (term, emb) in enumerate(aatc_lookup.items()):
    if i < 5:
        print(f"Term: {term} | Embedding shape: {emb.shape}")
    else:
        break

print(f"~ {len(aatc_lookup)} AATC terms represented as embeddings ~")

# # Save the lookup dictionary
# import pickle
# with open("data/aatc_lookup.pkl", "wb") as f:
#     pickle.dump(aatc_lookup, f)
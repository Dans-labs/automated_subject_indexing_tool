"""
This script represents the controlled vocabulary terms as embeddings and saves them to a lookup dictionary.

Input: a ttl file with controlled vocabulary terms
Output: a lookup dictionary with terms as keys and embeddings as values, saved as a .pkl file

"""


# Import libraries
import rdflib
import logging
from openai import OpenAI


model = "AI4EOSC/Qwen/Qwen3-Embedding-4B"
api_url = "https://vllm.cloud.ai4eosc.eu"
api_key = "sk-oC6NO4ZgEx1MGOJlce5wJA"


def get_embeddings(keyword, model, api_key, api_url): 
    client = OpenAI(
        base_url = api_url,
        api_key = api_key
    )

    response = client.embeddings.create(
        input = keyword,
        model = model
        )
    
    return response.data[0].embedding



# Load model 
#logging.info(f"Using embeddings model: {model}")
print(f"Using embeddings model: {model}")

# Read the turtle file 
path = "../data/aatc.ttl"

g = rdflib.Graph()
g.parse(path, format="turtle")

print("done reading ttl data!")


print("creating embeddings for the terms...")

labels = {}
notes = {}
aatc_lookup = {}


for s, p, o in g:
    if p.endswith("prefLabel") and o.language == "en":
        labels[s] = o
    if p.endswith("scopeNote"):
        notes[s] = o

results = []
for s, label in labels.items():
    note_text = notes.get(s, None)
    #print(label)
    full_text = f"{label}, {note_text}"

    vec = get_embeddings(full_text, model, api_key, api_url) # note: key = term label only, value = embedding for label + scope note 
    aatc_lookup[str(label)] = vec



# print first 5 items
for i, (term, emb) in enumerate(aatc_lookup.items()):
    if i < 5:
        print(f"Term: {term} | Embedding shape: {len(emb)}")
    else:
        break

print(f"~ {len(aatc_lookup)} AATC terms represented as embeddings ~")



# Save the lookup dictionary
import pickle
with open("../aatc_lookup_scopenotes.pkl", "wb") as f:
    pickle.dump(aatc_lookup, f)
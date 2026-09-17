"""
This script matches the embeddings of generated keywords to the closest controlled vocabulary terms using cosine similarity.

Input: list of keyword embeddings and lookup dictionary with controlled vocabulary terms as embeddings
Output: matched terms for each keyword based on highest similarity as a txt file

"""

import logging 
import pickle
import numpy as np
from src.utils.helpers import return_closest_term, return_top_n_terms




def run(config, keyword_embeddings):

    # options: "closest" or "top_n"
    matching_method = config["match_keywords_to_terms"]["matching_method"]


    # Load lookup dict (change path in default.yaml as needed)
    logging.info("Loading lookup dictionary...")
    lookup_dict_path = config["embeddings"]["lookup_dict_path"]
    lookup_dict = pickle.load(open(lookup_dict_path, "rb"))  # {term: embedding}

    terms = list(lookup_dict.keys())
    term_embeddings = np.stack(list(lookup_dict.values()))  # shape (num_terms, embedding_dim)

    if matching_method == "closest":
        logging.info("Using 'closest' matching method...")
        matched_terms_with_uris, cosines = return_closest_term(keyword_embeddings, term_embeddings, terms)
        # for t, c in zip(matched_terms_with_uris, cosines):
        #     print("term: ", t, "cosine: ", c)

    if matching_method == "top_n":
        logging.info("Using 'top_n' matching method...")
        matched_terms_with_uris, cosines = return_top_n_terms(config, keyword_embeddings, term_embeddings, terms, n=5)


    return matched_terms_with_uris, cosines


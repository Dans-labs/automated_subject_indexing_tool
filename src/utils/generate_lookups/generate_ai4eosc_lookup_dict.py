"""
Run this script when you're using the AI4EOSC platform. 
This script represents the controlled vocabulary terms as embeddings and saves them to a lookup dictionary.
A Qwen model is used in this script. 

Input: a ttl file with controlled vocabulary terms
Output: a lookup dictionary with terms as keys and embeddings as values, saved as a .pkl file

"""


# Import libraries
import rdflib
import logging
from openai import OpenAI
import yaml 
import argparse


def load_config(config_path: str) -> dict:
    """
    Load configuration from a YAML file.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg



def main(): 
    # Parse optional CLI argument for config file
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", 
        type=str, 
        default="src/configs/ai4eosc.yaml", 
        help="Path to the configuration YAML file."
    )
    # Optional CLI argument for DOI 
    parser.add_argument(
        "--doi",
        type=str,
        help="DOI to process."
    )
    args = parser.parse_args()

    # Load config 
    config = load_config(args.config)

    model = config["model"]["embeddings_model"]
    api_url = config["model"]["api_url"]
    api_key = config["model"]["api_key"]


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
    path = "code/asi/data/aatc.ttl"

    g = rdflib.Graph()
    g.parse(path, format="turtle")

    print("done reading ttl data!")


    # create lookup dictionary for AATC concepts
    print("working on creating the lookup dict!")
    aatc_lookup = {}
    for s, p, o in g:
        if p.endswith("prefLabel"):
            if o.language == "en":
                #aatc_lookup[str(o)] = str(s)
                # add embedding 
                vec = get_embeddings(str(o), model, api_key, api_url)
                aatc_lookup[str(o)] = vec

    # print first 5 items
    for i, (term, emb) in enumerate(aatc_lookup.items()):
        if i < 5:
            print(f"Term: {term} | Embedding shape: {len(emb)}")
        else:
            break

    print(f"~ {len(aatc_lookup)} AATC terms represented as embeddings ~")

    # Save the lookup dictionary
    import pickle
    with open(f"code/asi/data/aatc_{model}_lookup.pkl", "wb") as f:
        pickle.dump(aatc_lookup, f)



if __name__ == "__main__":
    main()


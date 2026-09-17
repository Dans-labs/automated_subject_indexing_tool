"""
Input: a list of keywords

Output: embeddding representations of the keywords (as lists)

"""


# Import libraries
import logging
from openai import OpenAI


def run(config, keywords):

    logging.info("Converting keywords to embeddings...")

    platform = config["model"]["platform"]
    model = config["model"]["embeddings_model"]
    api_url = config["model"]["api_url"]
    api_key = config["model"]["api_key"]
    

    keywords = [kw.lower() for kw in keywords]

        
    if platform == "ai4eosc": 

        def get_embeddings(keyword):

            client = OpenAI(
                base_url = api_url,
                api_key = api_key
            )

            response = client.embeddings.create(
                input = keyword,
                model = model
                )
            
            return response.data[0].embedding

        embeddings = [get_embeddings(kw) for kw in keywords]
        return embeddings
    


    if platform == "huggingface":
        from sentence_transformers import SentenceTransformer
        import numpy as np

        model = SentenceTransformer(config['model']['embeddings_model'])

        def get_embedding(text: str) -> np.ndarray:
            if not text or not isinstance(text, str):
                raise ValueError("Input text must be a non-empty string.")
            embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
            return embedding  # returns a NumPy array


        # Get embeddings
        keyword_embeddings = [get_embedding(kw) for kw in keywords]
        
        return keyword_embeddings

    else:
        logging.error(f"No embeddings function available for: {platform}")
        return None

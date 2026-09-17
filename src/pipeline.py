# src/my_nlp_tool/pipeline.py

import argparse 
import yaml
import logging 

import time

from src.tasks import extract_metadata

start = time.perf_counter()


#from .tasks import doi_to_md, generate_keywords, keywords_to_embeddings, match_keywords_to_terms
from src.tasks import generate_keywords, keywords_to_embeddings, match_keywords_to_terms, format_output
# Configure logging 
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


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
        default="src/configs/demo_ai4eosc.yaml", 
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
    #logging.info(f"Loaded configuration from {args.config}")

    if args.doi:
        doi = args.doi
    else: 
        doi = config["input"]["doi"]
        


    # Run tasks 
    logging.info("> Starting pipeline...")

    # Task 1: DOI to Metadata
    metadata_output = extract_metadata.run(config, doi)
    if metadata_output:
        print("\n=== METADATA ===")
        print(metadata_output)
        print("=======================\n")

    else: 
        logging.warning("No metadata was returned.")


    # Task 2: Generate keywords 

    if metadata_output:
        keywords = generate_keywords.run(config, metadata_output)
        if keywords:
            logging.info(f"> Keywords successfully generated!")
            print("\n=== GENERATED KEYWORDS ===")
            print(keywords)
            print("==========================\n")
        else:
            logging.warning("No keywords were generated.")


    # Task 3: Keywords to embeddings

    if keywords:
        keyword_embeddings = keywords_to_embeddings.run(config, keywords)
        if keyword_embeddings:
            logging.info(f"> Keyword embeddings successfully generated!")
            print("\n=== KEYWORD EMBEDDINGS ===")
            for i, emb in enumerate(keyword_embeddings):
                print(f"Keyword: {keywords[i]} | Embedding length: {len(emb)}")
            print("==========================\n")
        else:
            logging.warning("No keyword embeddings were generated.")



    # Task 4: Match keywords to terms

    if keyword_embeddings:
        logging.info("> Matching keywords to controlled vocabulary terms...")
        closest_matches, cosines = match_keywords_to_terms.run(config, keyword_embeddings)

    elapsed = time.perf_counter() - start

    # Task 5: Format output
    if metadata_output and keywords and closest_matches:
        metadata_length = len(metadata_output)
        format_output.run(config, keywords, closest_matches, cosines, metadata_length, metadata_output, doi, elapsed)

    logging.info("> Pipeline completed")
    #logging.info("===================================")
    print("\n")


if __name__ == "__main__":
    main()





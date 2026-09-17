
import pandas as pd
import logging
import os 

def run(config, keywords, matched_terms, cosines, metadata_length, metadata_output, doi, elapsed): 

    """
    Format the output of the pipeline into a csv with the columns [DOI, Keyword, Matched Term, URI, Cosine Similarity]
    
    
    Input: 
    - doi: the DOI of the publication
    - keywords: list of generated keywords
    - matched_terms: list of matched controlled vocabulary terms with URIs

    Output:
    - formatted_output: a dictionary containing the DOI, keywords, and matched terms with URIs
    """

    #doi = config["doi_to_md"]["doi"]
    platform = config["model"]["platform"]
    cosine_threshold = config["entity_matching"]["cosine_threshold"]
    matching_method = config["entity_matching"]["matching_method"]


    # Aggregate data for all keywords

    aggregated_data = []


    if matching_method == "closest":
        for keyword, matches, cosine in zip(keywords, matched_terms, cosines):
            if cosine >= cosine_threshold:
                # each `matches` is a list with exactly one (term, uri) tuple
                term, uri = matches[0]

                aggregated_data.append({
                    "DOI": doi,
                    "Metadata": metadata_output,
                    "Keyword": keyword,
                    "Matched Term": term,
                    "URI": uri,
                    "Cosine Similarity": float(cosine),   
                })

                print("========================================")
                print(f"{keyword} | {term} | {uri} | {cosine}")


    if matching_method == "top_n":        
        for i, keyword in enumerate(keywords):
            for (term, uri), cosine in zip(matched_terms[i], cosines[i]):
                if cosine >= cosine_threshold:
                    aggregated_data.append({
                        "DOI": doi,
                        "Metadata": metadata_output,
                        "Keyword": keyword,
                        "Matched Term": term,
                        "URI": uri,
                        "Cosine Similarity": float(cosine), 
                    })

                    
    print("========================================")

    # Create a DataFrame from the collected data
    aggregated_df = pd.DataFrame(aggregated_data)

    # Prepare the output values
    base_path_agg = config["output"]["base_path_keywords_aggregated"]
    output_path_agg = base_path_agg.replace("{platform}", platform)
    output_path_agg = output_path_agg.replace("{cosine_threshold}", str(cosine_threshold))

    # Check if the output file already exists
    if os.path.exists(output_path_agg):
        aggregated_df.to_csv(output_path_agg, mode='a', header=False, index=False)
    else:
        aggregated_df.to_csv(output_path_agg, index=False)

    
    ## Save run info
    run_info = {
        "DOI": [doi],
        "Platform": [platform],
        "Number of metadata characters": [metadata_length],
        "Number of matched terms": [len(aggregated_data)],
        "Matching method": [matching_method],
        "Cosine similarity threshold": [cosine_threshold],
        "Embedding model": [config["model"]["embeddings_model"]] ,
        "Instruct model": [config["model"]["instruct_model"]],
        "Runtime (seconds)": [elapsed]
    }

    run_info_df = pd.DataFrame(run_info)
    base_path_run = config["output"]["base_path_run_info"]
    output_path_run = base_path_run.replace("{doi}", doi.replace("/", "_"))
    output_path_run = output_path_run.replace("{platform}", platform)

    if os.path.exists(output_path_run):
        run_info_df.to_csv(output_path_run, mode='a', header=False, index=False)
    else:
        run_info_df.to_csv(output_path_run, index=False)

    
    return {"status": "success"}

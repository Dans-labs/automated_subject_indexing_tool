
import pandas as pd
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
    method = config["embeddings"]["method"]
    cosine_threshold = config["match_keywords_to_terms"]["cosine_threshold"]
    matching_method = config["match_keywords_to_terms"]["matching_method"]


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



    # Check if the output file already exists
    base_path_agg = config["format_output"]["base_path_keywords_aggregated"]
    output_path_agg = base_path_agg.replace("{method}", method)


    if os.path.exists(output_path_agg):
        aggregated_df.to_csv(output_path_agg, mode='a', header=False, index=False)
    else:
        aggregated_df.to_csv(output_path_agg, index=False)

    
    ## Save run info
    run_info = {
        "DOI": [doi],
        "Number of Metadata Characters": [metadata_length],
        "Number of Matched Terms": [len(aggregated_data)],
        "Matching Method": [matching_method],
        "Cosine Similarity Threshold": [cosine_threshold],
        "Embedding Method": [method],
        "LLM Model": [config["generate_keywords"]["model"]],
        "Runtime (seconds)": [elapsed]
    }

    run_info_df = pd.DataFrame(run_info)
    base_path_run = config["format_output"]["base_path_run_info"]
    output_path_run = base_path_run.replace("{doi}", doi.replace("/", "_"))

    if os.path.exists(output_path_run):
        run_info_df.to_csv(output_path_run, mode='a', header=False, index=False)
    else:
        run_info_df.to_csv(output_path_run, index=False)


    # # Save the DataFrame to a CSV file
    # base_path = config["format_output"]["base_path"]
    # output_path = base_path.replace("{doi}", doi.replace("/", "_"))
    # output_path = output_path.replace("{method}", method)
    # output_path = output_path.replace("{cosine}", str(cosine_threshold))


    return {"status": "success"}

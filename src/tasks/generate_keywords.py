
"""
Input: prompt text, dataset description

Output: a list of keywords

"""

# Import libraries
import logging 
import requests


def run(config, metadata):

    logging.info("> Generating keywords using LLM...")

    import os

    api_key = os.getenv("MY_API_KEY")
    if not api_key:
        raise RuntimeError("Missing API key! Set MY_API_KEY in your environment.")


    # Load config
    #api_key = config["generate_keywords"]["api_key"]
    api_url = config["generate_keywords"]["api_url"]
    model = config["generate_keywords"]["model"]
    prompt_template = config["prompts"]["generate_keywords"]

    # Format prompt with metadata
    prompt = prompt_template.replace("{metadata}", metadata)

    

    # Set up Hugging Face APi

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    def query(payload):
        response = requests.post(api_url, headers=headers, json=payload)
        return response.json()

    response = query({
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ],
        "model": f"{model}"
    })


    llm_response = response["choices"][0]["message"]["content"]
    # lower case the response
    llm_response = llm_response.lower()



    ### Process LLM response to extract keywords
    # process response 

    def unpack_response(llm_response):

        """
        Process the response from the LLM and extract the terms.
        Returns a list of terms.
        """
        # Split the response by commas
        terms = llm_response.split(',')
        # Strip whitespace and return the list of terms
        processed_keys = [term.strip() for term in terms]


        return processed_keys

    unpacked_response = unpack_response(llm_response)
    
    return unpacked_response
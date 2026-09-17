
"""
Input: prompt text, dataset description

Output: a list of keywords

"""

# Import libraries
import logging 
from openai import OpenAI
import requests


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


def get_keywords_openai(base_url, api_key, model, prompt): 

    client = OpenAI(
        base_url = base_url,
        api_key = api_key,
    )

    completion = client.chat.completions.create(
        model = model, 
        messages=[{"role":"user", "content": f"{prompt}"}], 
        temperature=1

    )

    return completion.choices[0].message.content


def get_keywords_huggingface(api_url, api_key, model, prompt):

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

    return response["choices"][0]["message"]["content"]


def run(config, metadata):

    logging.info("> Generating keywords using LLM...")

    # Load config
    platform = config["model"]["platform"]
    api_key = config["model"]["api_key"]
    base_url = config["model"]["api_url"]
    model = config["model"]["instruct_model"]
    prompt_template = config["prompts"]["generate_keywords"]

    # Insert metadata into prompt
    prompt = prompt_template.replace("{metadata}", metadata)

    if platform == "ai4eosc":
        llm_response = get_keywords_openai(base_url, api_key, model, prompt)
 
    if platform == "huggingface": 
        llm_response = get_keywords_huggingface(base_url, api_key, model, prompt)

    # Lower case the response
    llm_response = llm_response.lower()

    # Process/unpack the response into a list of keywords
    unpacked_response = unpack_response(llm_response)
    
    return unpacked_response
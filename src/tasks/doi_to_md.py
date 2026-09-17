
"""
This script takes the DOI of a dataset and collects its metadata

Input: dataset DOI
Output: metadata string with title and description

"""

import requests
import logging



def run(config, doi): 

    logging.info("> Fetching metadata from DOI...")

    #doi = config['doi_to_md']['doi']
    base_url = config["doi_to_md"]["base_url"]

    logging.info(f"Using DOI: {doi}")

    # Format DOI for URL
    doi_encoded = doi.replace(":", "%3A")
    #logging.info(f"Encoded DOI: {doi_encoded}")
    metadata_url = f"{base_url}{doi_encoded}"
    #logging.info(f"Metadata URL: {metadata_url}")

    #logging.info("Requesting metadata from API...")

    # Get metadata from API
    try:  
        response = requests.get(metadata_url)
        response.raise_for_status()
        metadata = response.json()

    except Exception as e:
        logging.error(f"Error fetching metadata for DOI: {e}")
        return None

    # Extract basic metadata
    try:
        title = metadata["ore:describes"]["title"]
        if isinstance(metadata["ore:describes"]["citation:dsDescription"], list):
            description = " ".join([desc["citation:dsDescriptionValue"].strip("<p>").strip("</p>") for desc in metadata["ore:describes"]["citation:dsDescription"]])
            description = description.replace("\n", "")
        else:
            description = metadata["ore:describes"]["citation:dsDescription"]["citation:dsDescriptionValue"]
            description = description.strip("<p>").strip("</p>")
            description = description.replace("\n", "")
    except KeyError as e:
        logging.error(f"Missing expected metadata fields: {e}")
        return ""
    

    # # Extract notes 
    # try: 
    #     notes = metadata["ore:describes"]["citation:notesText"]
    # except KeyError:
    #     notes = ""


    # # Extract series 
    # try: 
    #     series = metadata["ore:describes"]["citation:series"]["citation:seriesInformation"]
    #     series = series.strip("<p>").strip("</p>")
    # except KeyError:
    #     series = ""


    # # Extract keywords
    # def extract_keywords(metadata):

    #     try: 
    #         keywords = metadata["ore:describes"]["citation:keyword"]
    #         # extract all keywords as a string, seperated by commas
    #         if isinstance(keywords, list):
    #             keywords = [kw["citation:keywordValue"] for kw in keywords]
    #         else:
    #             keywords = [keywords["citation:keywordValue"]]
    #         return ", ".join(keywords)

    #     except KeyError:
    #         logging.info("No keywords found in metadata.")
    #         return None

    metadata_output = f"{title} {description}"

    # if notes is not None:
    #     metadata_output = f"{title} {description} {notes}"
    # elif series is not None:
    #     metadata_output = f"{title} {description} {series}"
    # else:
    #     metadata_output = f"{title} {description}"

    logging.info("> Metadata fetched successfully.")
    return metadata_output

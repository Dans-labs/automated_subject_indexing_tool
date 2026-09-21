# Automated Subject Indexing tool 
This tool automatically suggests keywords from a controlled vocabulary based on the content of the metadata of a dataset. The input is a dataset DOI and the output is a .csv file with the suggested terms and corresponding URIs. 

Current status: prototype, in active development.


## Table of Contents
- [Automated Subject Indexing tool](#automated-subject-indexing-tool)
  - [Table of Contents](#table-of-contents)
  - [Method](#method)
  - [Installation and Setup](#installation-and-setup)
  - [Usage](#usage)
  - [Configuration](#configuration)
  - [License](#license)
  - [AI statement](#ai-statement)


## Method
The task consist of two main components: 
- Summarizing the content of the dataset with keywords.
- Entity linking: linking the generated keywords to controlled vocabulary terms with resolvable URIs.



![System setup](docs/imgs/asi_overview_transparent.svg)
> *Figure 1: Overview of the ASI Tool.*


The controlled vocabulary that is currently used is a [flat representation](https://github.com/DANS-KNAW/Getty-AAT-Concepts/tree/main) of the Getty Art & Architecture Thesaurus (AAT). 

The tool uses the following technologies: 
- An LLM (currently Mistral-Small-3.1) for the generation of keywords.
- Contextualized embeddings to represent both the generated keywords and the vocabulary terms, allowing for entity linking. 

LLMs are a useful approach for summarizing the contents of a dataset in keywords, but appear unsuitable for the task of linking those keywords to controlled vocabulary terms. For the entity linking part, a solution based on embedding representations is implemented. [Embeddings](https://en.wikipedia.org/wiki/Word_embedding) are machine-readable vector representations of text that encode semantic information. Representing both the controlled vocabulary terms and the generated keywords as embeddings allows for the use of cosine similarity to match the keywords with their closest neighbor in the controlled vocabulary. 

## Installation and Setup
1. Make sure you have Python installed. 
2. Clone this repository: `git clone git@github.com:Dans-labs/automated_subject_indexing_tool.git`
3. Install the dependencies: `pip install -r requirements.txt`, preferably in a virtual environment like [uv](https://docs.astral.sh/uv/pip/environments/). This may take several minutes.  
4. Retrieve an API token for access to the models. You can choose one of these platforms for model access (or configure  your own):
   - Huggingface: Get a User Access Token with at least Inference permissions from [huggingface](https://huggingface.co/settings/tokens)
   - AI4EOSC: Get an LLM API Key. 
5. Add the token the `config.yaml`, or to your environment by running `export MY_API_KEY="your-key-here"` in your terminal. 
6. Download the flat representation of AAT concepts [here](https://github.com/DANS-KNAW/Getty-AAT-Concepts/blob/main/aatc.ttl) (keep the name `aatc.ttl`), place it in the `data` folder. 
7. Run one of the scripts in `src/utils/generate_lookups` to create a lookup dictionary of AATC terms as embeddings, depending on your choice of platform. After running the script, you can find the lookup dictionary in the `data` folder. This only has to be done once. 


## Usage
1. Add your API key to one of the config templates
   1. For AI4EOSC, use `src/configs/template_ai4eosc.yaml` 
   2. For huggingface, use `src/configs/template_hf.yaml` 
2. Run the pipeline: `bash run_pipeline.sh`

## Configuration
You can customize the following settings in `src/configs/default.yaml`: 
- The instruct model (for keyword generation)
- The embeddings model (for entity linking) 
- The cosine threshold: only keyword-term pairs with a cosine similarity score higher than this number are added to the output file. 
- The prompt for keyword generation
- The keyword matching method. The options are 'closest' or 'top_n'. 'closest' retrieves only the single closest keyword-term pair, while 'top_n' allows you to specify the number of terms to be returned (as long as their cosine similarity is higher than the threshold.)


## License 
<!-- TO DO: add license info here-->
To be added. 

## AI statement 
- No AI was used in writing the documentation of this project. 
- No AI was used in writing the Python code. 
- AI (Mistral) was used to write the bash script. 
- AI was occasionally used to solve errors in the code (Mistral and Lumo). 

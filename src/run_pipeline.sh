#!/usr/bin/env bash
# ------------------------------------------------------------
# Run the ASI pipeline for every DOI listed in a .txt file.
#
# Expected layout of the DOI file (one DOI per line):
#   10.1234/abcde1
#   10.5678/fghij2
#
# Expected output:
#   - A CSV file with run information for each DOI
#   - A CSV file with aggregated keywords for all DOIs
# ------------------------------------------------------------

# Path to the file that holds the DOIs
DOI_FILE="data/input/demo/demo_dois.txt"
# Path to the config file
CONFIG_FILE="src/configs/demo_huggingface.yaml"


let COUNT=0

# Iterate over each line (each DOI) in the file.
# Using `while IFS= read -r` preserves whitespace and avoids word‑splitting.
while IFS= read -r DOI; do
    # Skip empty lines

    [[ -z "$DOI" ]] && continue

    let COUNT++
    echo ""
    echo ""
    echo "------------------------------------------------------------"
    echo "Processing item #$COUNT"

    echo "Processing DOI: $DOI"

    # Add DOI prefix
    DOI="doi:10.17026/$DOI"

    # Run the pipeline. Adjust the --doi and --config arguments as needed.
    python3 -m src.pipeline --doi "$DOI" --config "$CONFIG_FILE"

    # Check the exit status of the Python command
    if [[ $? -ne 0 ]]; then
        echo "Warning: Python script failed for DOI $DOI" >&2
    else
        echo "Finished processing DOI: $DOI"
    fi

    # # Every 8 items, pause for 5 minutes to avoid overloading services.
    # if (( COUNT % 6 == 0 )); then
    #     echo "Pausing for 5 minutes to avoid overloading API..."
    #     sleep 320
    # fi
done < "$DOI_FILE"  
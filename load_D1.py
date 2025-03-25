import argparse
import os
import subprocess
import json
from pathlib import Path

# URL of the dataset
DATASET_URL = "https://ftp-trace.ncbi.nlm.nih.gov/ReferenceSamples/giab/data_RNAseq/AshkenazimTrio/HG004_NA24143_mother/Baylor_PacBio/reads/m64139_220124_190646.hifi_reads.bam"

# Define metadata
metadata = {
    'platform': 'PacBio',
    'technology': 'IsoSeq'
}

# Download function
def download_data(url, output_dir):
    """Download file using wget if it doesn't already exist."""
    output_path = output_dir / Path(url).name
    if not output_path.exists():
        print(f"Downloading {url} to {output_path}...")
        subprocess.run(["wget", "-c", url, "-O", str(output_path)], check=True)
    else:
        print(f"File already exists: {output_path}, skipping download.")
    return output_path

# Create metadata file (JSON format)
def create_metadata_file(output_dir, metadata):
    """Save metadata to JSON file."""
    metadata_file = os.path.join(output_dir, 'dataset_metadata.json')
    with open(metadata_file, 'w') as outfile:
        json.dump(metadata, outfile, indent=4)
    print(f"Metadata saved to {metadata_file}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Download dataset and save metadata.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='Output directory where dataset files will be saved.', required=True)
    parser.add_argument('--name', type=str, help='Name of the dataset.', required=True)

    # Parse arguments
    args = parser.parse_args()

    # Create the output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Download the BAM file
    download_data(DATASET_URL, Path(args.output_dir))

    # Save metadata
    create_metadata_file(args.output_dir, metadata)

if __name__ == "__main__":
    main()



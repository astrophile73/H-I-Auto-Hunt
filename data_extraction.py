import pandas as pd
import os
import requests

# 1. Load the catalog
catalog_df = pd.read_csv('catalogue_malsdr3v1_all.csv')

# 2. Filter the catalog for the specific spectral window 'LSPW_10'
# Using .str.upper() ensures it matches regardless of case
lspw_10_df = catalog_df[catalog_df['spw_id'].str.upper() == 'LSPW_10']

# 3. Extract unique pointing and spectral window combinations for LSPW_10
unique_pointings = lspw_10_df[['pointing_name', 'spw_id']].drop_duplicates()

# 4. Define the base URL and output directory
base_url = "https://mals.iucaa.in/osdf/malsdr3v1/{}/{}/spectra.tgz?file_type=SPECTRAL"
output_dir = "mals_spectra_downloads_lspw_10"
os.makedirs(output_dir, exist_ok=True)

# 5. Loop through unique pointings and download the archives
for index, row in unique_pointings.iterrows():
    pointing = row['pointing_name']
    spw = row['spw_id']
    
    # Construct the download URL
    download_url = base_url.format(pointing, spw)
    
    # Define the local filename
    local_filename = f"{pointing}_{spw}_spectra.tgz"
    local_filepath = os.path.join(output_dir, local_filename)
    
    print(f"Downloading {local_filename}...")
    
    # Download the file
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status() # Check for HTTP errors
        
        with open(local_filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully saved to {local_filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {download_url}. Error: {e}")

print("LSPW_10 bulk download process completed.")
import os
import tarfile

# Use raw strings (r"") for Windows paths to avoid escape character errors
base_path = r"E:\Radio and Gamma-ray observational astronomy Data analysis projects\R2\R2"

# Update these folder names if you saved them differently
download_dir = os.path.join(base_path, "mals_spectra_downloads_lspw_10") 
extract_dir = os.path.join(base_path, "mals_spectra_extracted_lspw_10")

os.makedirs(extract_dir, exist_ok=True)

for filename in os.listdir(download_dir):
    if filename.endswith(".tgz") or filename.endswith(".tar.gz"):
        file_path = os.path.join(download_dir, filename)
        
        # Create a folder for each pointing to keep files organized
        pointing_folder_name = filename.replace("_spectra.tgz", "").replace(".tgz", "")
        pointing_extract_path = os.path.join(extract_dir, pointing_folder_name)
        os.makedirs(pointing_extract_path, exist_ok=True)
        
        print(f"Extracting {filename}...")
        try:
            with tarfile.open(file_path, "r:gz") as tar:
                tar.extractall(path=pointing_extract_path)
        except Exception as e:
            print(f"Failed to extract {filename}: {e}")
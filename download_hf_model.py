from huggingface_hub import snapshot_download

# Specify the repository ID and local directory where you want to download the model
repo_id = "openai/whisper-large-v3" 
download_folder = "/Users/minyoungcho/Downloads/TranscribeTube-main" 

snapshot_download(repo_id=repo_id, local_dir=download_folder)

print(f"Model repository has been downloaded to {download_folder}")
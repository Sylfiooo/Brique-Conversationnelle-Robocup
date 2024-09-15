from huggingface_hub import hf_hub_download
hf_hub_download(repo_id="ggerganov/whisper.cpp", filename="ggml-base.en.bin", local_dir="./src/stt/modele/", local_dir_use_symlinks=False)
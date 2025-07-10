from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="QuantFactory/Llama-3.2-3B-GGUF",
    filename="llama-3.2-3b.Q4_K_M.gguf",
    local_dir=".",
    local_dir_use_symlinks=False
)

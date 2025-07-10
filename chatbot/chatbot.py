from pathlib import Path
from edu import HybridInstantEduGPT

# Update this path as per your model location
MODEL_PATH = Path("models/llama-2-7b-chat.Q4_K_M.gguf")

bot = HybridInstantEduGPT(str(MODEL_PATH))

def get_chat_response(message: str) -> str:
    return bot.get_response(message)




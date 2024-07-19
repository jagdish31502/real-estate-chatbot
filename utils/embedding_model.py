from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from dotenv import load_dotenv
import os

# Load environment variables.
load_dotenv()

# Function for Initializing embedding model.
def embedding_model():
    try:
        Settings.embed_model = HuggingFaceEmbedding(model_name= os.getenv('EMBED_MODEL'))
        return Settings.embed_model
    
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        return f"Error loading embedding model: {e}"
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from dotenv import load_dotenv
import os

# Load environment variables.
load_dotenv()

 # add your GOOGLE API key here
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# Function for Initializing llm model
def llm_model():
    try:   
        Settings.llm = Gemini(model_name= os.getenv('GEMINI_MODEL'))
        return Settings.llm
    except Exception as e:
        print(f"Error initializing LLM model: {e}")
        return f"Error initializing LLM model: {e}"

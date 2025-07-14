from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
print("Loaded Key:", os.getenv("OPENAI_API_KEY"))

import os
from dotenv import load_dotenv

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

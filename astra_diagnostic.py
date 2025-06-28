import os
from dotenv import load_dotenv
import cassio
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Cassandra

#  Load .env 
load_dotenv()

ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

print(" Loaded environment variables.")
print(f"ASTRA_DB_ID: {ASTRA_DB_ID}")
print(f" ASTRA_DB_KEYSPACE: {ASTRA_DB_KEYSPACE}")

#  Initialize Cassio 
try:
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)
    print(" cassio.init successful.")
except Exception as e:
    print(f" cassio.init failed: {e}")
    exit(1)

#  Embeddings 
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#  Vector Store Setup 
try:
    astra_vector_store = Cassandra(
        embedding=embedding,
        table_name="diagnostic_table",  # Temporary test table
        session=None,
        keyspace=ASTRA_DB_KEYSPACE,
    )
    print(" Cassandra vector store initialized.")
except Exception as e:
    print(f" Failed to initialize Cassandra vector store: {e}")
    exit(1)

#  Test Document Insertion 
try:
    test_doc = Document(page_content="Hello from diagnostic script!", metadata={"source": "diagnostic"})
    result = astra_vector_store.add_documents([test_doc])
    print(f" Successfully inserted {len(result)} document(s).")
except Exception as e:
    print(f" Document insertion failed: {e}")
    exit(1)

print(" Done. Now check your Astra DB > Keyspace > Tables > 'diagnostic_table'")

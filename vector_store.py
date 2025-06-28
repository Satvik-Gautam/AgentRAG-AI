import os
from dotenv import load_dotenv
import cassio
from langchain_core.documents import Document
from langchain_community.vectorstores import Cassandra
from langchain_huggingface import HuggingFaceEmbeddings

# Load env variables
load_dotenv()

ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

# Init cassio connection
cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)

# Embedding model
embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
# Create Cassandra vector store
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="PROJECT_TABLE",  # Your table name
    session=None,
    keyspace=ASTRA_DB_KEYSPACE,
)

# Store documents in the vector store
def store_documents(documents):
    print(f" Attempting to store {len(documents)} documents to Astra DB...")

    # Get hashes of current documents in the DB
    try:
        existing_docs = astra_vector_store.similarity_search("", k=1000)  # fetch a large number
        existing_hashes = set(
            doc.metadata.get("hash") for doc in existing_docs if "hash" in doc.metadata
        )
    except Exception as e:
        print(f" Failed to fetch existing documents: {e}")
        existing_hashes = set()

    # Filter only new docs (i.e., hash not in DB)
    new_docs = [doc for doc in documents if doc.metadata.get("hash") not in existing_hashes]

    if not new_docs:
        print(" All documents already exist. No new chunks to insert.")
        return []

    try:
        inserted_chunks = astra_vector_store.add_documents(new_docs)
        print(f"Successfully inserted {len(inserted_chunks)} new chunks.")
        return inserted_chunks
    except Exception as e:
        print(f" Failed to store documents: {e}")
        raise


# Get retriever
def get_retriever():
    return astra_vector_store.as_retriever()

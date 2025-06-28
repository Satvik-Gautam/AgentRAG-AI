import fitz
import os
import requests
import hashlib
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load env vars
load_dotenv()
USER_AGENT = os.getenv("USER_AGENT", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": USER_AGENT}

def load_from_url(url: str):
    """Custom URL loader with user-agent"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract just visible text
        text = soup.get_text(separator="\n", strip=True)
        return [Document(page_content=text, metadata={"source": "user", "type": "url", "url": url})]
    except Exception as e:
        print(f" Failed to load {url}: {e}")
        return []

def load_from_pdf(file_path: str):
    doc = fitz.open(file_path)
    text = "".join([page.get_text() for page in doc]) # type: ignore
    doc.close()
    return [
        Document(page_content=text, metadata={"source": "user", "type": "pdf", "filename": os.path.basename(file_path)})
    ]

def load_default_documents():
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]
    docs = []
    for url in urls:
        docs.extend(load_from_url(url))
    return docs

 
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,          # characters, not tokens
        chunk_overlap=100,        # better continuity
        separators=["\n\n", "\n", ".", " "]  # priority of splitting
    )

    chunks = splitter.split_documents(documents)
    
    filtered_chunks = []
    for chunk in chunks:
        content = chunk.page_content.strip()
        if content:
            # Generate SHA256 hash based on content
            hash_val = hashlib.sha256(content.encode("utf-8")).hexdigest()
            chunk.page_content = content
            chunk.metadata["hash"] = hash_val
            filtered_chunks.append(chunk)

    print(f" Split into {len(filtered_chunks)} clean chunks.")
    return filtered_chunks


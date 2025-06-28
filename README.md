# 🧠 AgentRAG AI — An Agentic RAG System with Contextual Intelligence

AgentRAG AI is an advanced Retrieval-Augmented Generation (RAG) framework designed to empower applications with the ability to reason, retrieve, and respond accurately using both private (user-uploaded) and public (web-searched) knowledge. Built with modern LLM orchestration tools and integrated vector databases, this system goes beyond simple question-answering by intelligently deciding where to route user queries—either to a vector DB for document-based responses or to the web for real-time factual answers. It offers modularity, efficiency, and high customizability, serving as a powerful base for building production-ready AI assistant tools.
This project brings together the power of LangChain, LLMs from Groq (Gemma/DeepSeek), Astra DB as a vector store, and Tavily as a web search engine, forming a full-fledged agentic pipeline for grounded response generation.

---

### Hugging Face Space
- Try the live demo of the AI Agentic RAG application on Hugging Face Spaces: [HuggingFace Space Link](https://huggingface.co/spaces/SATVIKGAUTAM/AI-AgenticRAG)

---

## 📌 Project Overview

**AgentRAG AI** is a fully agentic, production-grade Retrieval-Augmented Generation (RAG) system designed to intelligently answer user queries by dynamically retrieving information from either private documents (uploaded by the user) or real-time web content.

The project addresses a common challenge in AI question-answering systems: how to provide reliable, context-aware, and up-to-date responses across both static and dynamic knowledge domains.

### 🎯 Objectives
The primary objective is to provide a proof-of-concept for an AI-powered AgentRAG that can:
- ✅ Enable users to upload their own documents (PDFs, URLs, articles) and query them using natural language.
- ✅ Route user questions intelligently—based on their nature—to either the local document vector database or real-time web search.
- ✅ Prevent duplicate data storage using hash-based deduplication.
- ✅ Generate accurate, context-grounded answers using powerful LLMs (e.g., DeepSeek/ Gemma via Groq API).
- ✅ Provide an intuitive, responsive UI via Streamlit for seamless interaction.

### 🔑 Key Features
| Feature                           | Description                                                                                                               |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| 🔄 **Dynamic Query Routing**      | Uses a fine-tuned LLM to decide whether a question should be answered from private documents or live web search.          |
| 📎 **Custom Document Loader**     | Supports uploading PDFs, adding URLs, and loading default expert articles.                                                |
| 🧠 **Context-Aware LLM Response** | Final answers are generated using retrieved context and a strong LLM (via Groq), ensuring high-quality, faithful outputs. |
| 🧩 **Chunking & Deduplication**   | Documents are split into chunks with recursive splitting and hashed to prevent re-insertion of duplicates into the DB.    |
| 🌐 **Web Search via Tavily**      | If a question needs up-to-date public knowledge, the system fetches relevant content from the web using Tavily API.       |
| 💽 **Vector Store Integration**   | Uses Astra DB as a scalable, efficient vector store to store and search over embedded chunks.                             |
| ⚡ **Modular Graph Execution**     | The whole logic is built using a node-based structure—route → retrieve/web → generate—easy to extend and debug.           |
| 📊 **Streamlit UI**               | Provides a clean, interactive interface to upload files, input queries, and view system decisions & final answers.        |

---

## 🔁 Project Flow
The AgentRAG AI system operates through a clean, modular, and intelligent multi-step pipeline, ensuring high accuracy and performance across different types of user queries.

📂 1. **Document Ingestion (Optional by User)**

Users can upload documents or URLs to be used as private context for future questions.
PDF Upload: Users select PDF files from their device.
URL Submission: Users paste URLs (e.g., blog posts or documentation).
Default Articles: Pre-loaded expert URLs are also included by default for testing purposes.
These documents are processed via:
- ✅ BeautifulSoup (for HTML cleaning)
- ✅ PyMuPDF (for reading PDFs)
- ✅ LangChain Document class wrapping each input
- ✅ RecursiveCharacterTextSplitter to chunk text into smaller sections (with overlap for context preservation)

🔍 2. **Deduplication & Vectorization**
Before inserting documents into the vector store:
- 🔐 Each chunk is hashed using SHA256.
- 🧠 Only new unique chunks (not already present in the DB by hash) are stored—avoids costly duplication.
- 📦 Chunks are embedded using HuggingFace's all-MiniLM-L6-v2 model.
- 🏦 Stored in Astra DB (Cassandra-based vector store) using LangChain’s Cassandra wrapper.

❓ 3. **User Query Input**
When a user types a question into the app:
- The system wraps this query into a GraphState (a LangGraph-compatible state dictionary).
- This state is passed into the graph nodes to route the question and eventually generate a response.

🧭 4. **Question Routing (Router Node)**
The system dynamically determines where to look for the answer:
- Uses a fine-tuned router model (LLM) to classify the query as:
   - "retrieve" → Private vector DB
   - "web_search" → External web search (Tavily) This enables agentic decision-making based on user intent.

📥 5. **Context Retrieval**

a. From Vector DB
- If routed to "retrieve":
- User question is embedded using the same embedding model.
- Similar vectors are retrieved from Astra DB.
- These are used as context for generation.

b. From Web (Tavily)
- If routed to "web_search":
- Tavily API fetches real-time web documents.
- System extracts and filters useful content fields only (ignores titles, URLs, metadata).
- This ensures only clean, relevant knowledge is passed to the LLM.

✨ 6. **Answer Generation (RAG)**

- Retrieved context is used to create a custom prompt.
- Prompt template:
      - Answer the following question using the context provided below.
      - If the answer is not in the context, respond with "I don't know."
      - Context:
      - combined retrieved content]
      - Question: [user query]
- Prompt is sent to DeepSeek LLM via Groq API.

🖥️ 7. **User Interface via Streamlit**
All interactions happen on a beautiful Streamlit frontend:
- Upload document / enter URL
- Type question
- View system route decision
- See retrieved sources (context)
- Final answer output
- Live feedback on insertions, duplicates, etc.

---

## 🛠 Tech Stack and Technologies Used
AgentRAG AI integrates a modern, scalable, and modular tech stack built specifically for intelligent retrieval-augmented generation (RAG) workflows with agentic capabilities. Each tool has been purposefully chosen to address a specific functionality in the pipeline:

⚙️ 1. **Python 3.12**
- Core programming language.
- Used for data ingestion, processing, routing, generation, and backend logic.
- Supported by a rich ecosystem of AI, NLP, and data libraries.

📦 2. **Streamlit**
- Frontend framework to create interactive, real-time UIs without HTML/CSS.
- Allows users to:
- Upload documents or URLs
- Ask questions
- View source retrievals and generated answers
- Enables rapid prototyping and deployment of AI-powered web apps.

📚 3. **LangChain (Core, Community, and Integration Libraries)**
- Orchestrator for multi-step LLM workflows.
- Handles:
- Document loading (Document, TextSplitter)
- Retrieval via Retriever interface
- Graph-based workflow management (GraphState, Runnable)
- LLM abstraction and agent routing

🧠 4. **Hugging Face Transformers & Embeddings**
- Embedding Model: all-MiniLM-L6-v2
- Converts text chunks into high-dimensional vector space for semantic search.
- Hugging Face provides highly optimized, open-source transformer models used for embedding and retrieval.

💾 5. **Astra DB (Vector DB using Cassandra)**
- A serverless, cloud-native vector database powered by Apache Cassandra.
- Used to store:
- Embedded document vectors
- Associated metadata and SHA256 content hashes (for deduplication)
- Enables high-speed vector search with low-latency response time.

🌐 6. **Tavily Search API**
- Real-time, web search engine API for live answers from the internet.
- Used when no relevant internal document matches the user query.
- Ensures the model can answer latest news, events, or global facts outside of uploaded PDFs or URLs.

🧭 7. **LangGraph Router (Graph-based Reasoning)**
- A lightweight decision-making agent.
- Decides whether to fetch answer from:
- Private Vector DB (retrieve)
- Web Search API (web_search)
- Adds agentic intelligence to route user questions dynamically.

🔐 8. **SHA256 Hashing (via hashlib)**
- Every chunk is hashed based on its content.
- Helps detect and skip previously stored chunks, reducing storage cost and redundancy.
- Guarantees that only new, unique content enters the vector DB.

🧾 9. **PyMuPDF (fitz)**
- Efficient PDF text extractor.
- Handles parsing multi-page documents for user-uploaded content.
- Works well with large files and provides cleaner extraction than older libraries.

🌍 10. **BeautifulSoup (bs4)**
 -Parses raw HTML from user-supplied URLs.
- Extracts clean, readable text while removing scripts, ads, styles, etc.
- Converts any blog or article into pure text for downstream chunking.

💬 11. **Groq LLMs (e.g., DeepSeek-Llama 70B via ChatGroq)**
- Ultra-fast inference for final answer generation.
- Used to perform reasoning and answer generation with context retrieved from documents or web.
- Groq’s speed ensures near real-time performance, even for large prompts.

---

## 🗂️ Project Structure

- AgentRAG-AI/
- │
- ├── .venv/                         # Python virtual environment (excluded from GitHub)
- ├── .env                           # Environment variables (API keys, DB config, etc.)
- ├── README.md                      # 📘 Project documentation (this file)
- ├── requirements.txt              # Python package dependencies
- ├── streamlit_app.py              # 🎛️ Main Streamlit web application entry point
- │
- ├── RAG/                           # 📦 Core logic and components
- │   ├── __init__.py                # Python package initializer
- │   ├── config.py                  # 🔐 API keys and configuration variables
- │   ├── document_loader.py         # 📄 Load & parse PDFs and URLs into LangChain documents
- │   ├── vector_store.py            # 💾 AstraDB vector store integration + deduplication
- │   ├── router.py                  # 🧭 Question router (decides vector vs web)
- │   ├── graph_logic.py             # 🔁 LangGraph logic for RAG pipeline
- │   ├── tools.py                   # 🧰 Web search tools (Tavily Search API integration)
- │
- ├── assets/                        # 📂 Optional directory to store test documents (PDFs, etc.)
- │   └── example.pdf                # Sample user-uploaded PDF for testing
- │
- └── logs/                          # 📁 (Optional) folder for logging/storing debug info
    - └── app.log                    # Streamlit + vector store debug logs

📄 **File-by-File Descriptions**

| File               | Description                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------- |
| `.venv/`           | Your Python virtual environment. Should be in `.gitignore`.                                 |
| `.env`             | Environment-specific secrets (e.g., API keys, DB tokens).                                   |
| `requirements.txt` | Lists all Python dependencies (Streamlit, LangChain, Hugging Face, etc.).                   |
| `streamlit_app.py` | Entry point of the Streamlit UI. Handles file uploads, questions, and graph flow execution. |
| `README.md`        | Full documentation of the AgentRAG AI project (this file).                                  |

📦 **RAG/ Core Logic Folder**

| File                 | Description                                                                                                                                                            |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__init__.py`        | Initializes the folder as a Python package (may be empty).                                                                                                             |
| `config.py`          | Loads `.env` secrets like GROQ keys, Tavily token, and Astra DB config.                                                                                                |
| `document_loader.py` | Handles PDF and URL loading, parsing, and chunking using `fitz`, `BeautifulSoup`, and LangChain splitters. Also adds `SHA256` hashing to chunks to prevent duplicates. |
| `vector_store.py`    | Creates connection to Astra DB via `cassio`. Performs deduplicated document storage and embedding using HuggingFace.                                                   |
| `router.py`          | Routes user questions based on type to either `retrieve` (vector DB) or `web_search` (Tavily).                                                                         |
| `graph_logic.py`     | Defines the full LangGraph DAG logic, manages question routing, document retrieval, and LLM-based answer generation using context.                                     |
| `tools.py`           | Integrates with Tavily Search API. Handles content extraction from search results and formats them for LangChain consumption.                                          |

---

### ✅ Prerequisites

- Python 3.8 or higher  
- FFmpeg (for any media processing, optional)  
- PortAudio (for microphone input, optional if voice input is used)  
- A Groq API Key – [Get it here](https://console.groq.com/)  
- A Tavily API Key – [Get it here](https://app.tavily.com/)  
- An Astra DB Token + Database ID – [Sign up at DataStax](https://www.datastax.com/astra)  
- Git installed on your system  
- [AgentRAG AI GitHub Repository](https://github.com/your-username/AgentRAG-AI)

---

### ⚙️ Installation Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Satvik-Gautam/AgentRAG-AI.git
   cd AgentRAG-AI
2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
 3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
 4. **Add Your Environment Variables:**
    ```bash
    ASTRA_DB_ID=your_astra_db_id
    ASTRA_DB_APPLICATION_TOKEN=your_astra_token
    ASTRA_DB_KEYSPACE=your_keyspace
    GROQ_API_KEY=your_groq_api_key
    TAVILY_API_KEY=your_tavily_api_key
    USER_AGENT=your_custom_user_agent
  5. **Run the Application:**
     ```bash
     streamlit run streamlit_app.py

---

### 🧪 Usage

Once the app is running, you can interact with **AgentRAG AI** through a simple and intuitive web interface.

#### 🟢 Upload Your Knowledge:
- **PDF Upload**: Upload any research paper, book, or document.
- **URL Input**: Paste any webpage link to scrape and embed its content.
- The system automatically splits, hashes, and checks for duplicates before storing content in **Astra DB Vector Store** to prevent redundant uploads.

#### ❓ Ask Questions:
- Type any question in the input box (e.g., "What is a Transformer?", "Who won the World Test Championship in 2025?")
- The system intelligently **routes your query**:
  - If the answer is in your uploaded documents → it performs **context-aware RAG**.
  - If not → it performs a **real-time web search** using **Tavily AI**.

#### 🧠 Answer Generation:
- The system uses **Groq’s LLM (Gemma-2 / DeepSeek)** to generate concise, grounded answers using retrieved context.
- Only the final answer is shown – no unnecessary “<think>” thoughts or verbose LLM commentary.

#### 🔁 Repeated Use:
- You can upload multiple documents and URLs. Each new session builds on top of previous ones unless already deduplicated.
- Your queries can be short, long, vague, or technical – the system adapts using its routing and grounding logic.

---

### Example Use Cases:

- 📰 Ask questions on news reports or documents you've uploaded.
- 📄 Analyze technical PDFs or whitepapers by asking summary or insight-based questions.
- 🌐 Get up-to-date answers even beyond your uploaded context using Tavily.
- 🧪 Test your own AI knowledge base with personal or open-source datasets.

---

### 📜 License
 - This project is licensed under the MIT License. See the LICENSE file for details.

---

### 🙏 Acknowledgments

This project would not have been possible without the incredible contributions of open-source tools, platforms, and research that form the foundation of **AgentRAG AI**. Special thanks to:

- **LangChain** – For enabling powerful, modular RAG pipelines and seamless integration of tools like vector stores, LLMs, and agents.
- **Groq** – For providing ultra-fast inference and efficient language models like Gemma-2 and DeepSeek via the GroqCloud API.
- **Hugging Face** – For offering high-quality sentence embedding models (like `all-MiniLM-L6-v2`) used for document vectorization.
- **Tavily AI** – For enabling real-time web search functionality with high-precision result parsing to answer live user queries.
- **Astra DB (DataStax)** – For providing a scalable and serverless Cassandra-powered vector database to store and retrieve dense document embeddings.
- **Streamlit** – For making it easy to build interactive UIs with minimal code, enabling rapid deployment of AI-powered tools.
- **PyMuPDF / fitz** – For PDF parsing and extracting structured text from uploaded documents.
- **BeautifulSoup** – For clean and efficient HTML text extraction from URLs for user-added content.
- **Open Source Research Community** – Especially authors like [Lilian Weng](https://lilianweng.github.io) for publishing deeply informative research posts that served as initial input for testing and embedding.

> 💡 This project is a tribute to the open-source ecosystem and aims to empower developers, researchers, and learners to build practical and scalable Retrieval-Augmented Generation systems.

---

### 📬 Contact

If you have any questions, feedback, or suggestions regarding **AgentRAG AI**, feel free to reach out:

- **Developer:** Satvik Gautam  
- **Email:** satvikgautam07@gmail.com  
- **GitHub:** [@Satvik-Gautam](https://github.com/Satvik-Gautam)  
- **LinkedIn:** [Satvik Gautam](https://www.linkedin.com/in/satvik-gautam)

Contributions, issues, and feature requests are always welcome!  
If you find this project useful, please consider giving it a ⭐ on [GitHub](https://github.com/Satvik-Gautam/AgentRAG-Ai).

---


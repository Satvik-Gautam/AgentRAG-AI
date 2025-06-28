from typing import List
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from vector_store import get_retriever
from tools import web
from router import question_router
from config import GROQ_API_KEY

retriever = get_retriever()

# Define state structure
class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[Document]

# LLM setup
llm = ChatGroq(model="deepseek-r1-distill-llama-70b")

# RAG-style generate
def generate_answer(question: str, documents: List[Document]) -> str:
    context = "\n".join([doc.page_content for doc in documents if isinstance(doc, Document)])

    prompt = f"""Answer the following question **strictly using the context provided**.
Avoid explanations, thoughts, or assumptions. Just give a clear and concise answer.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {question}
Answer:"""

    response = llm.invoke(prompt)
    return str(getattr(response, "content", response)).strip()



# Node: Retrieve from Vector DB + Generate Answer
def retrieve(state: GraphState) -> GraphState:
    print(" RETRIEVE NODE")
    question = state["question"]
    documents = retriever.invoke(question)

    answer = generate_answer(question, documents)

    return {
        "question": question,
        "documents": documents,
        "generation": answer,
    }

# Node: Wiki Search + Generate Answer
def web_search(state: GraphState) -> GraphState:
    print(" TAVILY WEB SEARCH NODE")
    question = state["question"]
    
    results = web.invoke({"query": question})
    docs = []

    # ✅ New: Extract content from Tavily's "results" list
    if isinstance(results, dict) and "results" in results:
        for item in results["results"]:
            if isinstance(item, dict) and "content" in item:
                docs.append(
                    Document(page_content=item["content"], metadata={"source": item.get("url", "Tavily")})
                )
    else:
        print("⚠️ Unexpected Tavily result format:", results)

    # 🧠 Now pass real web content to the LLM
    answer = generate_answer(question, docs)

    return {
        "question": question,
        "documents": docs,
        "generation": answer,
    }


# Node: Router (Vector DB or Wiki)
def route_question(state: GraphState) -> str:
    print(" ROUTE NODE")
    question = state["question"]
    source = question_router.invoke({"question": question})

    if isinstance(source, dict):
        route = source.get("datasource", "web_search")
    else:
        route = getattr(source, "datasource", "web_search")

    print(f"Routing Decision: {route}")
    return "web_search" if route == "web_search" else "retrieve"

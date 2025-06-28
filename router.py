from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from langchain_groq import ChatGroq
from config import GROQ_API_KEY

llm = ChatGroq(model="llama-3.3-70b-versatile")

class RouteQuery(BaseModel):
    datasource : Literal["vectorstore" ,"web_search"] = Field(
        ...,description ="Route to VectorStore(default/docs) or Web_Search(web_search)"
    )

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """
You are an expert router in a retrieval-augmented generation (RAG) system.

Route user questions to the appropriate datasource.

- Use the vectorstore if the question relates to the documents in it, which include:
  • Topics like LLM agents, prompt engineering, adversarial attacks
  • Any custom URLs or PDFs recently added by the user

- Use Web Search if the question is about unrelated topics.

Always prefer the vectorstore if the user's documents were recently added.
"""
route_prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])

question_router = route_prompt | structured_llm_router



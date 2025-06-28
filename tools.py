# tools.py

from langchain_tavily import TavilySearch
from langchain_core.tools import Tool
from config import TAVILY_API_KEY

# Tavily tool that returns list of dicts with "content" and metadata
tavily = TavilySearch(k=3)

# Wrap as LangChain Tool
web = Tool.from_function(
    name="tavily-search",
    func=tavily.invoke,
    description="Web search tool using Tavily. Accepts a 'query' and returns top results.",
)

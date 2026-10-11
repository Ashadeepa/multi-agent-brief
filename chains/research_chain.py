"""Chain 1: user request -> web search tool -> research notes."""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

from .llm import get_llm
from .search_tool import web_search

RESEARCH_PROMPT = ChatPromptTemplate.from_template(
    """You are a Research Analyst. The request below may be a comparison, a market sizing, a
company review or an open question - adapt to it.

Using ONLY the web search results provided, write structured research notes:
- Group facts by theme (e.g. financials, products/pipeline, market position, news).
- Give concrete figures and dates where available.
- Put the source URL in brackets after every fact.
- If the request compares entities, cover each one evenly.
- Do NOT invent facts; say plainly where the results are silent.

Request: {request}

Search results:
{search_results}

Research notes:"""
)


def build_research_chain():
    """Input: {"request"}. Output: {"request", "search_results", "research"}."""
    search = RunnablePassthrough.assign(
        search_results=RunnableLambda(lambda x: web_search(x["request"]))
    )
    write = RESEARCH_PROMPT | get_llm() | StrOutputParser()
    return search | RunnablePassthrough.assign(research=write)

"""Chain 2: research notes -> key findings, gaps, risks."""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from .llm import get_llm

ANALYSIS_PROMPT = ChatPromptTemplate.from_template(
    """You are a Strategy Analyst reviewing research notes for a decision-maker.

Produce, in this order:
1. Key findings - the 4-6 insights that matter most to the request, each with its evidence.
2. Missing information - what the research does NOT cover that a decision needs.
3. Risks - for each: what it is, who it affects, likelihood (low/med/high) and impact.
4. Implications - what the findings and risks mean for the request.

Be critical: separate facts from inference and flag weak or single-source evidence.

Request: {request}

Research notes:
{research}

Analysis:"""
)


def build_analysis_chain():
    """Input: dict with "request", "research". Adds "analysis"."""
    return RunnablePassthrough.assign(
        analysis=ANALYSIS_PROMPT | get_llm() | StrOutputParser()
    )

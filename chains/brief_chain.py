"""Chain 3: analysis -> executive brief."""
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from .llm import get_llm

BRIEF_PROMPT = ChatPromptTemplate.from_template(
    """You are writing a one-page brief for a senior executive who has two minutes.
Plain language, no jargon, lead with the answer. Use EXACTLY these markdown headings in order:

## Executive Summary
(3 sentences max: the answer, why, and what to do.)
## Key Findings
(3-5 bullets, each one line.)
## Risks
(3-5 bullets, each tagged High/Medium/Low.)
## Recommendations and Next Steps
(Numbered, action-oriented, with an owner type or timeframe where possible.
Answer everything the request asks, e.g. if it asks for three options give three.)

Mention important gaps in the evidence briefly under Risks.

Request: {request}

Analysis:
{analysis}

Executive brief:"""
)


def build_brief_chain():
    """Input: dict with "request", "analysis". Adds "brief"."""
    return RunnablePassthrough.assign(
        brief=BRIEF_PROMPT | get_llm() | StrOutputParser()
    )

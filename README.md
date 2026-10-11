# Multi-Agent Research & Executive Brief

Ask a business question (e.g. "Compare Pfizer's performance with Johnson & Johnson") and get a
one-page executive brief. Three LangChain chains run in sequence, each feeding the next:

1. **Research** (`chains/research_chain.py`) - web search tool (DuckDuckGo, no key) -> research notes
2. **Analysis** (`chains/analysis_chain.py`) - key findings, missing information, risks
3. **Brief** (`chains/brief_chain.py`) - executive summary, findings, risks, recommendations

`MAS_LangChain.py` is the backend pipeline; `app.py` is the Streamlit dashboard on top of it.

## Run

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY=...        # required (optional: GEMINI_MODEL, default gemini-3.6-flash)
export SERP_API_KEY=...          # optional: SerpAPI search; falls back to DuckDuckGo
streamlit run app.py             # dashboard
python MAS_LangChain.py          # or run the backend from the CLI
```

## Known limitation

Search uses short result snippets, so briefs can lack hard figures. Fetching full pages would improve depth.

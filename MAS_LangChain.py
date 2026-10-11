"""Multi-agent research & executive brief: research -> analysis -> brief (3 chained chains)."""
from chains.analysis_chain import build_analysis_chain
from chains.brief_chain import build_brief_chain
from chains.research_chain import build_research_chain


def run_workflow_full(request: str) -> dict:
    """Return request, search_results, research, analysis, brief."""
    request = request.strip()
    if not request:
        raise ValueError("Request is empty")
    # Each chain's output is the next chain's input.
    pipeline = build_research_chain() | build_analysis_chain() | build_brief_chain()
    return pipeline.invoke({"request": request})


def run_workflow(request: str) -> str:
    """Return the executive brief as markdown text."""
    return run_workflow_full(request)["brief"]


if __name__ == "__main__":
    print(run_workflow("Compare Pfizer's performance with Johnson & Johnson."))

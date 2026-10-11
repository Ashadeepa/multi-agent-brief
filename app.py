import re
import time

import streamlit as st

from MAS_LangChain import run_workflow_full

SECTIONS = ["Executive Summary", "Key Findings", "Risks", "Recommendations and Next Steps"]
PRESETS = {
    "Pfizer vs J&J": "Compare Pfizer's performance with Johnson & Johnson: financials, pipeline, "
    "market position. Identify risks and recommend what Pfizer's leadership should prioritise.",
    "AI training in India": "Research demand for AI Literacy and AI Training among Indian Enterprises. "
    "Find relevant industry reports, identify common enterprise use cases and recommend three "
    "service offerings worth validating with potential customers.",
    "Custom": "",
}


def split_sections(text: str) -> dict:
    parts = re.split(r"^#{1,4}\s*(.+?)\s*$", text, flags=re.MULTILINE)
    return {parts[i].strip().strip("*"): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def get_section(sections: dict, name: str) -> str:
    return next((v for k, v in sections.items() if k.lower().startswith(name.lower()[:12])), "")


def parse_sources(search_results: str) -> list:
    return re.findall(r"\[(\d+)\] (.*)\nURL: (\S*)", search_results)


st.set_page_config(page_title="Research & Action Brief", page_icon="📊", layout="wide")
st.markdown(
    """<style>
    .block-container {padding-top: 2rem;}
    div[data-testid="stMetric"] {background: rgba(128,128,128,.08); padding: 12px 16px; border-radius: 10px;}
    </style>""",
    unsafe_allow_html=True,
)
st.session_state.setdefault("history", [])
st.session_state.setdefault("result", None)

with st.sidebar:
    st.header("📊 Brief Studio")
    preset = st.selectbox("Starting point", list(PRESETS))
    st.caption("Pipeline: Search → Research → Analysis → Executive Brief")
    st.divider()
    st.subheader("History")
    if not st.session_state["history"]:
        st.caption("No briefs yet.")
    for i, item in enumerate(reversed(st.session_state["history"])):
        if st.button(item["request"][:48] + "…", key=f"h{i}", use_container_width=True):
            st.session_state["result"] = item

st.title("Multi-Agent Research & Executive Brief")
request = st.text_area(
    "Business question", value=PRESETS[preset], height=110, key=f"q_{preset}",
    placeholder="e.g. How is Pfizer performing relative to J&J?",
)

if st.button("Generate brief", type="primary", disabled=not request.strip()):
    start = time.time()
    try:
        with st.status("Running agents...", expanded=True) as status:
            st.write("🔎 Searching the web, researching, analysing, drafting brief...")
            res = run_workflow_full(request)
            res["seconds"] = time.time() - start
            status.update(label=f"Done in {res['seconds']:.0f}s", state="complete", expanded=False)
        st.session_state["result"] = res
        st.session_state["history"].append(res)
    except Exception as e:
        st.error(f"Workflow failed: {e}")

res = st.session_state["result"]
if res:
    sections = split_sections(res["brief"])
    sources = parse_sources(res["search_results"])
    risks = [l for l in get_section(sections, "Risks").splitlines() if l.strip()]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sources", len(sources))
    c2.metric("Risks flagged", len(risks))
    c3.metric("Brief words", len(res["brief"].split()))
    c4.metric("Run time", f"{res.get('seconds', 0):.0f}s")

    tab_brief, tab_research, tab_analysis, tab_sources = st.tabs(
        ["📝 Executive Brief", "🔬 Research", "🧮 Analysis", "🔗 Sources"]
    )
    with tab_brief:
        with st.container(border=True):
            st.subheader("Executive Summary")
            st.markdown(get_section(sections, "Executive Summary") or res["brief"])
        left, right = st.columns(2)
        with left, st.container(border=True):
            st.subheader("Key Findings")
            st.markdown(get_section(sections, "Key Findings"))
        with right, st.container(border=True):
            st.subheader("⚠️ Risks")
            st.markdown(get_section(sections, "Risks"))
        with st.container(border=True):
            st.subheader("Recommendations and Next Steps")
            st.markdown(get_section(sections, "Recommendations"))
        st.download_button("⬇️ Download brief (.md)", res["brief"], "executive_brief.md")
    with tab_research:
        st.markdown(res["research"])
    with tab_analysis:
        st.markdown(res["analysis"])
    with tab_sources:
        for n, title, url in sources:
            st.markdown(f"{n}. [{title}]({url})")
    st.info("Review sources and validate recommendations before using them for real decisions.")
else:
    st.info("Pick a starting point or type a question, then click **Generate brief**.")

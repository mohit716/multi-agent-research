# app.py

import streamlit as st
from agents.planner import run_planner
from agents.executor import run_executor
from agents.supervisor import run_supervisor

st.set_page_config(page_title="Multi-Agent Research", page_icon="🤖", layout="centered")
st.title("🤖 Multi-Agent Research Assistant")
st.caption("Powered by LangGraph + Claude")

# --- initialize session state ---
if "subtasks" not in st.session_state:
    st.session_state.subtasks = []
if "results" not in st.session_state:
    st.session_state.results = []
if "final_report" not in st.session_state:
    st.session_state.final_report = ""
if "research_done" not in st.session_state:
    st.session_state.research_done = False
if "approved" not in st.session_state:
    st.session_state.approved = False

# --- Input ---
topic = st.text_input("Enter a research topic:", placeholder="e.g. LangGraph multi-agent systems")

if st.button("🔍 Run Research", disabled=not topic):
    # reset state on new run
    st.session_state.subtasks = []
    st.session_state.results = []
    st.session_state.final_report = ""
    st.session_state.research_done = False
    st.session_state.approved = False

    # --- Planner ---
    with st.status("🔵 Planner Agent: Breaking topic into subtasks...") as planner_status:
        st.session_state.subtasks = run_planner(topic)
        st.write("**Subtasks identified:**")
        for i, task in enumerate(st.session_state.subtasks):
            st.write(f"{i+1}. {task}")
        planner_status.update(label="🔵 Planner Agent: Done ✅", state="complete")

    # --- Executor ---
    with st.status("🟡 Executor Agent: Searching and summarizing...") as executor_status:
        st.session_state.results = run_executor(st.session_state.subtasks)
        st.write("**Research summaries:**")
        for i, result in enumerate(st.session_state.results):
            with st.expander(f"Result {i+1}: {st.session_state.subtasks[i][:60]}..."):
                st.write(result)
        executor_status.update(label="🟡 Executor Agent: Done ✅", state="complete")

    st.session_state.research_done = True

# --- Human Checkpoint (only show if research is done and not yet approved) ---
if st.session_state.research_done and not st.session_state.approved:
    st.divider()
    st.subheader("⏸️ Human Checkpoint")
    st.write("Review the research summaries. Approve to generate the final report.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Generate Report"):
            st.session_state.approved = True
            st.rerun()
    with col2:
        if st.button("🔄 Reject & Re-run"):
            st.session_state.research_done = False
            st.rerun()

# --- Supervisor (only runs after approval) ---
if st.session_state.approved and not st.session_state.final_report:
    with st.status("🟢 Supervisor Agent: Compiling final report...") as supervisor_status:
        st.session_state.final_report = run_supervisor(topic, st.session_state.results)
        supervisor_status.update(label="🟢 Supervisor Agent: Done ✅", state="complete")

# --- Show final report if ready ---
if st.session_state.final_report:
    st.divider()
    st.subheader("📄 Final Report")
    st.markdown(st.session_state.final_report)
    st.download_button(
        label="⬇️ Download Report",
        data=st.session_state.final_report,
        file_name=f"research_report.md",
        mime="text/markdown"
    )
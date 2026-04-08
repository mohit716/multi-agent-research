# 🤖 Multi-Agent Research Assistant

A production-grade multi-agent AI system built with LangGraph and Claude, deployed on Streamlit Cloud.

🔗 **Live Demo:** https://multi-agent-research-guvzsdeapp8f5qeu4xsmcjx.streamlit.app/

---

## Architecture

Uses a **Planner → Executor → Human Checkpoint → Supervisor** agent pattern:

- 🔵 **Planner Agent** — breaks a research topic into 3 focused subtasks using Claude
- 🟡 **Executor Agent** — searches the web (DuckDuckGo) and summarizes each subtask using Claude
- ⏸️ **Human Checkpoint** — user reviews summaries and approves or rejects before proceeding
- 🟢 **Supervisor Agent** — compiles all summaries into a structured final report

---

## Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — stateful multi-agent orchestration
- [Anthropic Claude](https://anthropic.com) — LLM for planning, summarization, and report generation
- [DuckDuckGo Search](https://pypi.org/project/ddgs/) — web search for each subtask
- [Streamlit](https://streamlit.io) — UI and deployment

---

## Project Structure

```
multi-agent-research/
├── app.py              # Streamlit UI with live agent status updates
├── graph.py            # LangGraph orchestration and state management
├── agents/
│   ├── planner.py      # Breaks topic into 3 focused subtasks
│   ├── executor.py     # Web search + Claude summarization per subtask
│   └── supervisor.py   # Compiles all summaries into final report
├── requirements.txt
└── .env                # API key (not committed)
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/mohit716/multi-agent-research
cd multi-agent-research
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Create a `.env` file**
```
ANTHROPIC_API_KEY=your_key_here
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## Features

- Live agent step visualization in the UI
- Human-in-the-loop approval checkpoint before final report generation
- Expandable per-subtask research summaries
- Downloadable final report as markdown
- Stateful agent orchestration using LangGraph shared state

---

## How It Works

1. User enters a research topic
2. **Planner Agent** calls Claude to break the topic into 3 subtasks
3. **Executor Agent** loops through each subtask — searches DuckDuckGo, sends results to Claude for summarization
4. UI pauses at **Human Checkpoint** — user reviews summaries and approves or rejects
5. On approval, **Supervisor Agent** calls Claude to compile all summaries into a structured final report
6. Report is displayed in the UI and available for download as a `.md` file

---

## Agent State (LangGraph)

All agents share a common state object passed through the graph:

```python
class ResearchState(TypedDict):
    topic: str            # user input
    subtasks: List[str]   # planner output
    results: List[str]    # executor output
    approved: bool        # human checkpoint
    final_report: str     # supervisor output
```

---

## Deployment

Deployed on [Streamlit Community Cloud](https://streamlit.io/cloud) with API key managed via Streamlit Secrets.

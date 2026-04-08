from agents.supervisor import run_supervisor
from agents.executor import run_executor
from agents.planner import run_planner
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

# --- Shared State (passed between all agents) ---
class ResearchState(TypedDict):
    topic: str                  # user input
    subtasks: List[str]         # planner output
    results: List[str]          # executor output
    approved: bool              # human checkpoint
    final_report: str           # supervisor output

# --- Node functions (empty for now) ---
def planner_node(state: ResearchState) -> ResearchState:
    """
    Calls the planner agent.
    Gets topic from state, adds subtasks back into state.
    """
    print(f"🔵 Planner running for topic: {state['topic']}")
    
    subtasks = run_planner(state["topic"])  # call Claude
    
    print(f"🔵 Planner produced: {subtasks}")
    
    return {**state, "subtasks": subtasks}  # update state with subtasks

def executor_node(state: ResearchState) -> ResearchState:
    """
    Takes subtasks from state.
    Runs search + summarize on each.
    Stores results back in state.
    """
    print(f"🟡 Executor running for {len(state['subtasks'])} subtasks")

    results = run_executor(state["subtasks"])

    print(f"🟡 Executor finished all subtasks")

    return {**state, "results": results}

def supervisor_node(state: ResearchState) -> ResearchState:
    """
    Takes topic + all results from state.
    Compiles into final report.
    Stores report back in state.
    """
    print(f"🟢 Supervisor compiling final report...")

    report = run_supervisor(state["topic"], state["results"])

    print(f"🟢 Supervisor done.")

    return {**state, "final_report": report}

def human_checkpoint(state: ResearchState) -> ResearchState:
    # will pause for approval
    return state

# --- Build the graph ---
def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("human_checkpoint", human_checkpoint)

    # flow: planner → executor → human_checkpoint → supervisor → END
    graph.set_entry_point("planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "human_checkpoint")
    graph.add_edge("human_checkpoint", "supervisor")
    graph.add_edge("supervisor", END)

    return graph.compile()
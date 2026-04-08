# test.py
from graph import build_graph

graph = build_graph()

result = graph.invoke({
    "topic": "LangGraph multi-agent systems",
    "subtasks": [],
    "results": [],
    "approved": False,
    "final_report": ""
})

print("\nSubtasks:")
for i, s in enumerate(result["subtasks"]):
    print(f"  {i+1}. {s}")

print("\nResults:")
for i, r in enumerate(result["results"]):
    print(f"\n  Result {i+1}:\n  {r}")


print("\nFinal Report:")
print(result["final_report"])
# agents/executor.py

import os
from anthropic import Anthropic
from ddgs import DDGS
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def search_web(query: str) -> str:
    """
    Searches DuckDuckGo for a query.
    Returns top 3 results combined as raw text.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))

    # combine title + body of each result into one string
    combined = ""
    for r in results:
        combined += f"Title: {r['title']}\n"
        combined += f"Body: {r['body']}\n\n"

    return combined


def summarize(query: str, raw_text: str) -> str:
    """
    Sends raw search results to Claude.
    Claude summarizes into 3-4 sentences relevant to the query.
    """
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": f"""You are a research assistant.

Based on the search results below, write a 3-4 sentence summary answering this query:
Query: {query}

Search Results:
{raw_text}

Write only the summary, nothing else."""
            }
        ]
    )

    return response.content[0].text.strip()


def run_executor(subtasks: list[str]) -> list[str]:
    """
    Loops through all subtasks.
    For each: searches web → summarizes → stores result.
    Returns list of summaries, one per subtask.
    """
    results = []

    for i, task in enumerate(subtasks):
        print(f"🟡 Executor searching subtask {i+1}: {task}")

        raw = search_web(task)           # step 1: search
        summary = summarize(task, raw)   # step 2: summarize
        results.append(summary)          # step 3: store

        print(f"🟡 Executor done with subtask {i+1}")

    return results
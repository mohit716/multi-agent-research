# agents/planner.py

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_planner(topic: str) -> list[str]:
    """
    Takes a research topic and breaks it into 3 focused subtasks.
    Returns a list of 3 strings.
    """

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""You are a research planner.
                
Break this topic into exactly 3 focused search subtasks:
Topic: {topic}

Reply ONLY as a numbered list, nothing else. Example:
1. subtask one
2. subtask two  
3. subtask three"""
            }
        ]
    )

    # get the raw text back from Claude
    raw = response.content[0].text

    # split into lines, strip numbers like "1. " from the front
    lines = raw.strip().split("\n")

    subtasks = [line.split(". ", 1)[-1].strip() for line in lines if line.strip()]

    return subtasks 
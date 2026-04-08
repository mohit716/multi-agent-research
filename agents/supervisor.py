# agents/supervisor.py

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def run_supervisor(topic: str, results: list[str]) -> str:
    """
    Takes the original topic and all executor summaries.
    Compiles them into one clean, structured final report.
    """

    # join all summaries into one block of text
    combined = ""
    for i, result in enumerate(results):
        combined += f"Research Section {i+1}:\n{result}\n\n"

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        messages=[
            {
                "role": "user",
                "content": f"""You are a senior research supervisor.

Compile the following research sections into one clean, well-structured report.

Topic: {topic}

{combined}

Format the report as:
# [Topic Title]

## Summary
2-3 sentence overview of the entire topic.

## Key Findings
3-5 bullet points of the most important insights.

## Conclusion
2-3 sentences wrapping up the research.

Write only the report, nothing else."""
            }
        ]
    )

    return response.content[0].text.strip()
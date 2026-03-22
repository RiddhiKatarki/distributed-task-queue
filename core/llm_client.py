from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("REDPILL_API_KEY"),
    base_url="https://api.redpill.ai/v1"
)


def generate_task_from_prompt(user_query: str) -> str:
    system_prompt = """
You are a task generator.

Convert user input into STRICT JSON format:

{
  "task_type": "<one of allowed tasks>",
  "payload": { ... },
  "priority": "low | default | high"
}

Allowed task_types:
- add_numbers
- fetch_market_data
- scrape_website
- cpu_heavy_task

Rules:
- Output ONLY valid JSON
- No explanation
- No markdown
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
    )

    return response.choices[0].message.content
import json
from registry import TASK_REGISTRY


def clean_json_output(output: str) -> str:
    if "```" in output:
        output = output.split("```")[1]
    return output.strip()


def parse_llm_output(output: str) -> dict:
    try:
        cleaned = clean_json_output(output)
        data = json.loads(cleaned)

        if "task_type" not in data:
            raise ValueError("Missing task_type")

        if data["task_type"] not in TASK_REGISTRY:
            raise ValueError("Invalid task_type")

        if "payload" not in data:
            data["payload"] = {}

        if "priority" not in data:
            data["priority"] = "default"

        return data

    except Exception as e:
        raise ValueError(f"Invalid LLM response: {e}")
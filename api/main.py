from fastapi import FastAPI
from models import task
from models.task import Task
from core.queue import enqueue_task
from core.redis_client import redis_client
import json

from pydantic import BaseModel
from fastapi import HTTPException

from core.llm_client import generate_task_from_prompt
from core.llm_parser import parse_llm_output

app = FastAPI()

from pydantic import BaseModel

class TaskRequest(BaseModel):
    task_type: str
    payload: dict
    priority: str = "default"

class LLMTaskRequest(BaseModel):
    query: str

@app.post("/tasks")
def create_task(req: TaskRequest):
    task = Task.create(req.task_type, req.payload)
    task.priority = req.priority
    enqueue_task(task.dict())

    redis_client.set(f"task:{task.task_id}", json.dumps({
        "status": "queued"
    }))

    return {"task_id": task.task_id}


@app.get("/tasks/{task_id}")
def get_status(task_id: str):
    data = redis_client.get(f"task:{task_id}")
    return json.loads(data) if data else {"error": "not found"}


@app.post("/llm-task")
def create_llm_task(req: LLMTaskRequest):
    try:
        # 1. Generate from LLM
        llm_raw_output = generate_task_from_prompt(req.query)

        print("LLM RAW OUTPUT:", llm_raw_output)

        # 2. Parse + validate
        task_data = parse_llm_output(llm_raw_output)

        # 3. Create internal task
        task = Task.create(
            task_data["task_type"],
            task_data["payload"]
        )

        task.priority = task_data.get("priority", "default")

        # 4. Enqueue
        enqueue_task(task.dict())

        # 5. Store initial state
        redis_client.set(f"task:{task.task_id}", json.dumps({
            "status": "queued",
            "source": "llm"
        }))

        return {
            "task_id": task.task_id,
            "parsed_task": task_data
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
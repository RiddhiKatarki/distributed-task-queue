from typing import Dict, Any
import uuid
import time
from pydantic import BaseModel

class Task(BaseModel):
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    retries: int = 0
    max_retries: int = 3
    status: str = "queued"
    created_at: float = time.time()
    priority: str = "default"

    @staticmethod
    def create(task_type: str, payload: Dict[str, Any]) -> 'Task':
        return Task(
            task_id=str(uuid.uuid4()),
            task_type=task_type,
            payload=payload,
            )
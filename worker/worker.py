import time
import json
from core.queue import dequeue_task, enqueue_task
from registry import TASK_REGISTRY
from core.redis_client import redis_client

def execute_task(task):
    task_id = task["task_id"]

    try:
        redis_client.set(f"task:{task_id}", json.dumps({
            "status": "running"
        }))

        func = TASK_REGISTRY.get(task["task_type"])
        if not func:
            raise Exception("Unknown task")

        result = func(task["payload"])

        redis_client.set(f"task:{task_id}", json.dumps({
            "status": "success",
            "result": result
        }))

    except Exception as e:
        task["retries"] += 1

        if task["retries"] <= task["max_retries"]:
            enqueue_task(task)
        else:
            redis_client.set(f"task:{task_id}", json.dumps({
                "status": "failed",
                "error": str(e)
            }))

def worker_loop():
    while True:
        task = dequeue_task()

        if not task:
            time.sleep(1)
            continue

        execute_task(task)

if __name__ == "__main__":
    worker_loop()
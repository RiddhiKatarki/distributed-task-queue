import json
from core.redis_client import redis_client

PRIORITY_QUEUES = {
    "high": "queue:high",
    "default": "queue:default",
    "low": "queue:low"
}

def enqueue_task(task: dict):
    queue_name = PRIORITY_QUEUES.get(task.get("priority", "default"))
    redis_client.rpush(queue_name, json.dumps(task))


def dequeue_task():
    for queue in ["high", "default", "low"]:
        task = redis_client.lpop(PRIORITY_QUEUES[queue])
        if task:
            return json.loads(task)
    return None
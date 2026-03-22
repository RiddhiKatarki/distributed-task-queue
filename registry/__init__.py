from tasks.sample_tasks import *

TASK_REGISTRY = {
    "add_numbers": add_numbers,
    "fetch_market_data": fetch_market_data,
    "cpu_heavy_task": cpu_heavy_task,
    "scrape_website": scrape_website
}
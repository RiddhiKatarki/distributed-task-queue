







## Features
- Distributed task execution using Redis
- Priority-based scheduling
- Retry with failure handling
- LLM-based task generation (natural language -> tasks)
- Web scraping + market data ingestion


## Run locally
- uvicorn api.main:app
- python -m worker.worker
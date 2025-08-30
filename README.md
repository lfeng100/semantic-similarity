# semantic-similarity
Flask service that exposes endpoints for **embeddings**, **similarity**, and **search** for sentence similarity. 
Runs locally and in Docker. Includes **OpenAPI docs** (`/docs`), **JSON logging**, **request IDs**, validation, and tests.
Provider is swappable: fast **stub** or real **E5** (from HuggingFace `intfloat/multilingual-e5-small`).

# Set up env
Project made in Python 3.11.0

(Optionally in venv)

```pip install -r requirements.txt```

Update .env as necessary to change model provider

# Run the app locally
```python .\app.py```

# Run the app in container
Ensure Docker engine is running

```
docker build -t semantic-similarity .
docker run --rm -p 8080:8080 --env-file .env semantic-similarity
```

# Test
```pytest -q```

# TODO (Potential Enhancements)
1. Model warm-up on startup to avoid first-request latency spikes.
1. Configurable log level (LOG_LEVEL) & structured error logs.
1. Rate limiting
1. CI
# semantic-similarity
Python API to return embeddings for given text

# Set up env
Project made in Python 3.11.0

(Optionally in venv)
```pip install -r requirements.txt```

# Run the app locally
```python .\app.py```

# Run the app in container
```
docker build -t semantic-similarity .
docker run --rm -p 8080:8080 semantic-similarity
```

# Test
```pytest -q```
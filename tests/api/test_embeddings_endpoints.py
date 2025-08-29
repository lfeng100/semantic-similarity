def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_get_embedding_requires_sentence(client):
    response = client.get("/embeddings")
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_get_embedding_success(client):
    response = client.get("/embeddings?sentence=hello+world")
    assert response.status_code == 200
    data = response.get_json()
    assert "embedding" in data and isinstance(data["embedding"], list)

def test_post_bulk(client):
    # empty body
    response = client.post("/embeddings/bulk")
    assert response.status_code == 400

    # not a list
    response = client.post("/embeddings/bulk", json={"sentences": "a random string"})
    assert response.status_code == 400

    # empty sentence
    response = client.post("/embeddings/bulk", json={"sentences": ["this is a sentence", "  "]})
    assert response.status_code == 400

    response = client.post("/embeddings/bulk", json={"sentences": ["this is a sentence", "this is another sentence"]})
    assert response.status_code == 200
    data = response.get_json()
    assert "embeddings" in data and len(data["embeddings"]) == 2

def test_post_similarity(client):
    # only one sentence
    response = client.post("/embeddings/similarity", json={"sentence_1": "this is the first sentence"})
    assert response.status_code == 400

    # empty sentence
    response = client.post("/embeddings/similarity", json={"sentence_1": "this is the first sentence", "sentence_2": "   "})
    assert response.status_code == 400

    response = client.post("/embeddings/similarity", json={"sentence_1": "this is the first sentence", "sentence_2": "this is the second sentence"})
    assert response.status_code == 200
    assert "similarity" in response.get_json()

def test_post_search(client):
    # missing sentences
    response = client.post("/embeddings/search", json={"query": "this is some query"})
    assert response.status_code == 400

    # missing query
    response = client.post("/embeddings/search", json={"sentences": ["this is a sentence","this is another sentence"]})
    assert response.status_code == 400

    # empty query
    response = client.post("/embeddings/search", json={"query": " ", "sentences": ["this is a sentence","this is another sentence"]})
    assert response.status_code == 400
    
    # empty sentences
    response = client.post("/embeddings/search", json={"query": "this is some query", "sentences": []})
    assert response.status_code == 400

    response = client.post("/embeddings/search", json={"query": "this is some query", "sentences": ["this is a sentence","this is another sentence"]})
    assert response.status_code == 200
    data = response.get_json()
    assert "top_result" in data and "similarity" in data

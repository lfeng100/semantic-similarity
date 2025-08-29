from lib.api import api_bp
from lib.utils.utils import error_response
from lib.api.models.EmbeddingsAPIModels import EmbeddingsBulkRequest, SimilarityRequest, SearchRequest

from flask import request
from pydantic import ValidationError

@api_bp.get("/ping")
def ping():
    return {"message": "pong"}, 200

# GET /embeddings
# query param: sentence
@api_bp.get("/embeddings")
def get_embedding():
    sentence = request.args.get("sentence", type=str)
    if not sentence:
        return error_response(400, "Missing required query parameter 'sentence'.")
    # placeholder response
    return {"embedding": [0.0, 0.0, 0.0]}, 200

# POST /embeddings/bulk
# payload: JSON with list of strings "sentences"
@api_bp.post("/embeddings/bulk")
def post_bulk():
    try:
        payload = request.get_json(force=True, silent=False)
        data = EmbeddingsBulkRequest.model_validate(payload)
    except (TypeError, ValueError):
        return error_response(400, "Invalid JSON body")
    except ValidationError as validation_error:
        return error_response(400, "Payload validation failed", validation_error.errors())


    embeddings = [[0.0, 0.0, 0.0] for _ in data.sentences]
    # placeholder response
    return {"embeddings": embeddings}, 200

# POST /embeddings/similarity
# payload: JSON with strings "sentence_1" and "sentence_2"
@api_bp.post("/embeddings/similarity")
def post_similarity():
    try:
        payload = request.get_json(force=True, silent=False)
        data = SimilarityRequest.model_validate(payload)
    except (TypeError, ValueError):
        return error_response(400, "Invalid JSON")
    except ValidationError as validation_error:
        return error_response(400, "Payload validation failed", validation_error.errors())

    # placeholder response
    return {"similarity": 0.0}, 200

# POST /embeddings/search
@api_bp.post("/embeddings/search")
# payload: JSON with string "query" and list of strings "sentences"
def post_search():
    try:
        payload = request.get_json(force=True, silent=False)
        data = SearchRequest.model_validate(payload)
    except (TypeError, ValueError):
        return error_response(400, "Invalid JSON")
    except ValidationError as validation_error:
        return error_response(400, "Payload validation failed", validation_error.errors())

    # placeholder response
    top = data.sentences[0] if data.sentences else ""
    return {"top_result": top, "similarity": 0.0}, 200

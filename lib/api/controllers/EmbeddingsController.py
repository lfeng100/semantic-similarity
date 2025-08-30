from lib.api import api_bp
from lib.utils.utils import error_response
from lib.api.models.EmbeddingsAPIModels import EmbeddingsBulkRequest, SimilarityRequest, SearchRequest
from lib.services.embeddings_service import embed_passage, embed_passages, similarity, search, get_provider
from lib.logging.structlog import log

from flask import request, current_app
from pydantic import ValidationError

@api_bp.get("/ping")
def ping():
    return {"message": "pong"}, 200

# readiness probe for provider
@api_bp.get("/ready")
def ready():
    provider = get_provider()

    log.info("ready check")
    return {
        "provider": provider.name or "Unknown",
        "loaded": provider.loaded,
        "dim": provider.dim or 0,
    }, 200

# GET /embeddings
# query param: sentence
@api_bp.get("/embeddings")
def get_embedding():
    sentence = request.args.get("sentence", type=str)
    if not sentence:
        log.error("embeddings fail")
        return error_response(400, "Missing required query parameter 'sentence'.")
    embedding = embed_passage(sentence)

    log.info("embeddings success")
    return {"embedding": embedding}, 200

# POST /embeddings/bulk
# payload: JSON with list of strings "sentences"
@api_bp.post("/embeddings/bulk")
def post_bulk():
    try:
        payload = request.get_json(force=True, silent=False)
        data = EmbeddingsBulkRequest.model_validate(payload)
    except (TypeError, ValueError):
        log.error("embeddings bulk fail")
        return error_response(400, "Invalid JSON body")
    except ValidationError as validation_error:
        log.error("embeddings bulk fail")
        return error_response(400, "Payload validation failed", validation_error.errors())

    max_sentences = current_app.config.get("MAX_BULK_SENTENCES")
    if len(data.sentences) > max_sentences:
        log.error("embeddings bulk fail")
        return error_response(413, "Too many sentences, max is: " + str(max_sentences))

    embeddings = embed_passages(data.sentences)

    log.info("embeddings bulk success")
    return {"embeddings": embeddings}, 200

# POST /embeddings/similarity
# payload: JSON with strings "sentence_1" and "sentence_2"
@api_bp.post("/embeddings/similarity")
def post_similarity():
    try:
        payload = request.get_json(force=True, silent=False)
        data = SimilarityRequest.model_validate(payload)
    except (TypeError, ValueError):
        log.error("embeddings similarity fail")
        return error_response(400, "Invalid JSON")
        log.error("embeddings similarity fail")
    except ValidationError as validation_error:
        return error_response(400, "Payload validation failed", validation_error.errors())

    similarity_score = similarity(data.sentence_1, data.sentence_2)

    log.info("embeddings similarity success")
    return {"similarity": similarity_score}, 200

# POST /embeddings/search
@api_bp.post("/embeddings/search")
# payload: JSON with string "query" and list of strings "sentences"
def post_search():
    try:
        payload = request.get_json(force=True, silent=False)
        data = SearchRequest.model_validate(payload)
    except (TypeError, ValueError):
        log.error("embeddings search fail")
        return error_response(400, "Invalid JSON")
    except ValidationError as validation_error:
        log.error("embeddings search fail")
        return error_response(400, "Payload validation failed", validation_error.errors())

    top_result, similarity_score = search(data.query, data.sentences)

    log.info("embeddings search success")
    return {"top_result": top_result, "similarity":similarity_score}, 200

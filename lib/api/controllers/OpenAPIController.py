from flask import request
from lib.api import api_bp

def _spec_servers():
    # Use the current request's origin as the server URL
    # e.g., http://localhost:8080
    base = request.host_url.rstrip("/")
    return [{"url": base}]

def _components():
    return {
        "schemas": {
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "integer"},
                            "message": {"type": "string"},
                            "details": {"nullable": True}
                        },
                        "required": ["code", "message"]
                    }
                },
                "required": ["error"]
            },
            "HealthResponse": {
                "type": "object",
                "properties": {"status": {"type": "string", "example": "ok"}},
                "required": ["status"]
            },
            "ReadyResponse": {
                "type": "object",
                "properties": {
                    "provider": {"type": "string", "example": "stub"},
                    "loaded": {"type": "boolean", "example": True},
                    "dim": {"type": "integer", "example": 8}
                },
                "required": ["provider", "loaded", "dim"]
            },
            "EmbeddingResponse": {
                "type": "object",
                "properties": {
                    "embedding": {
                        "type": "array",
                        "items": {"type": "number"},
                        "example": [0.12, -0.03, 0.99]
                    }
                },
                "required": ["embedding"]
            },
            "BulkEmbeddingsRequest": {
                "type": "object",
                "properties": {
                    "sentences": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1
                    }
                },
                "required": ["sentences"]
            },
            "BulkEmbeddingsResponse": {
                "type": "object",
                "properties": {
                    "embeddings": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"}
                        }
                    }
                },
                "required": ["embeddings"]
            },
            "SimilarityRequest": {
                "type": "object",
                "properties": {
                    "sentence_1": {"type": "string"},
                    "sentence_2": {"type": "string"}
                },
                "required": ["sentence_1", "sentence_2"]
            },
            "SimilarityResponse": {
                "type": "object",
                "properties": {"similarity": {"type": "number", "format": "float", "example": 0.73}},
                "required": ["similarity"]
            },
            "SearchRequest": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "sentences": {"type": "array", "items": {"type": "string"}, "minItems": 1}
                },
                "required": ["query", "sentences"]
            },
            "SearchResponse": {
                "type": "object",
                "properties": {
                    "top_result": {"type": "string"},
                    "similarity": {"type": "number", "format": "float", "example": 0.81}
                },
                "required": ["top_result", "similarity"]
            }
        }
    }

def _paths():
    return {
        "/health": {
            "get": {
                "summary": "Liveness",
                "responses": {
                    "200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/HealthResponse"}}}}
                }
            }
        },
        "/ready": {
            "get": {
                "summary": "Readiness",
                "responses": {
                    "200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ReadyResponse"}}}}
                }
            }
        },
        "/embeddings": {
            "get": {
                "summary": "Embed a single sentence",
                "parameters": [
                    {"in": "query", "name": "sentence", "required": True, "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {"description": "Vector", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/EmbeddingResponse"}}}},
                    "400": {"description": "Bad Request", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}}}
                }
            }
        },
        "/embeddings/bulk": {
            "post": {
                "summary": "Embed multiple sentences",
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BulkEmbeddingsRequest"},
                                                    "examples": {"basic": {"value": {"sentences": ["a", "b"]}}}}}
                },
                "responses": {
                    "200": {"description": "Vectors", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/BulkEmbeddingsResponse"}}}},
                    "400": {"description": "Validation Error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}}},
                    "413": {"description": "Too Large", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}}}
                }
            }
        },
        "/embeddings/similarity": {
            "post": {
                "summary": "Cosine similarity between two sentences",
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SimilarityRequest"},
                                                    "examples": {"basic": {"value": {"sentence_1": "a", "sentence_2": "b"}}}}}
                },
                "responses": {
                    "200": {"description": "Score", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SimilarityResponse"}}}},
                    "400": {"description": "Validation Error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}}}
                }
            }
        },
        "/embeddings/search": {
            "post": {
                "summary": "Search sentences by query similarity",
                "requestBody": {
                    "required": True,
                    "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SearchRequest"},
                                                    "examples": {"basic": {"value": {"query": "best dinner", "sentences": ["cozy trattoria", "late-night diner"]}}}}}
                },
                "responses": {
                    "200": {"description": "Top result", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/SearchResponse"}}}},
                    "400": {"description": "Validation Error", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/ErrorResponse"}}}}
                }
            }
        }
    }

def _openapi():
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Semantic Similarity API",
            "version": "1.0.0",
            "description": "Embeddings, similarity, and simple search."
        },
        "servers": _spec_servers(),
        "paths": _paths(),
        "components": _components()
    }

@api_bp.get("/openapi.json")
def openapi_json():
    return _openapi(), 200

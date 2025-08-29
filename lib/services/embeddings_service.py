from typing import List, Tuple
from flask import current_app
from lib.services.providers.stub_provider import StubProvider
from lib.utils.similarity import cosine_similarity

LOADED_PROVIDER = None

def get_provider():
    global LOADED_PROVIDER
    if LOADED_PROVIDER is not None:
        return LOADED_PROVIDER

    config = current_app.config
    name = config.get("EMBEDDINGS_PROVIDER")
    if name == "e5":
        from lib.services.providers.e5_provider import E5Provider
        LOADED_PROVIDER = E5Provider(
            model_name=config.get("EMBEDDING_MODEL_NAME"),
            device=config.get("EMBEDDING_DEVICE"),
        )
    else:
        LOADED_PROVIDER = StubProvider()
    return LOADED_PROVIDER

# utility functions
def embed_passage(sentence):
    provider = get_provider()
    return provider.embed_passages([sentence])[0]

def embed_passages(sentences):
    provider = get_provider()
    return provider.embed_passages(sentences)

def similarity(sentence_1, sentence_2):
    a = embed_passage(sentence_1)
    b = embed_passage(sentence_2)
    return cosine_similarity(a, b)

def search(query, sentences):
    provider = get_provider()
    query_vector = provider.embed_query(query)
    embeddings = provider.embed_passages(sentences)

    # look for highest score
    best_idx, best_score = -1, -1.0
    for idx, embedding in enumerate(embeddings):
        current_score = cosine_similarity(query_vector, embedding)
        if current_score > best_score:
            best_idx, best_score = idx, current_score

    return sentences[best_idx] if best_idx >= 0 else "", best_score if best_score >= 0.0 else 0.0

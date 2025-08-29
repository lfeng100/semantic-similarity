import os

class Config:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    TESTING = False
    JSON_SORT_KEYS = False # default is True

    EMBEDDINGS_PROVIDER = os.getenv("EMBEDDINGS_PROVIDER", "stub").lower() # provider: "stub" or "e5"
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "intfloat/multilingual-e5-small")
    EMBEDDING_DEVICE = os.getenv("EMBEDDING_DEVICE", "cpu") # "cpu" or "cuda"

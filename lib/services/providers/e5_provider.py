import numpy as np
from sentence_transformers import SentenceTransformer

# prefix "query: " and "passage: " to input texts?
class E5Provider:
    def __init__(self, model_name, device = "cpu"):
        self.name = "e5:" + model_name
        self.model = SentenceTransformer(model_name, device=device)
        self.loaded = True
        # run tiny encode to capture dim
        vec = self.embed_passages(["tiny example"])[0]
        self.dim = len(vec)

    def _to_list(self, arr):
        return arr.astype("float32").tolist()

    def embed_passages(self, sentences):
        inputs = []
        for sentence in sentences:
            inputs.append("passage:" + sentence.strip())

        embeddings = self.model.encode(
            inputs,
            normalize_embeddings=True,
            convert_to_numpy=True,
            batch_size=32
        )
        return [self._to_list(x) for x in embeddings]

    def embed_query(self, query):
        inp = "query:" + query.strip()
        embedding = self.model.encode(
            [inp],
            normalize_embeddings=True,
            convert_to_numpy=True,
            batch_size=1
        )[0]
        return self._to_list(embedding)

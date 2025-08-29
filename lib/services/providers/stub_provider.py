# stub for testing without loading model
class StubProvider:
    name = "stub"
    loaded = True
    dim = 8

    # replicates the deterministic embeddings of e5
    def hash_vector(self, text):
        accumulator = [0.0] * self.dim
        for idx, character in enumerate(text):
            accumulator[idx % self.dim] += float(ord(character)) # use unicode
        # L2-normalize so cosine similarity is well-behaved
        norm = sum(x*x for x in accumulator) ** 0.5
        return [x / norm for x in accumulator]

    def embed_passages(self, sentences):
        embeddings = []
        for sentence in sentences:
            embeddings.append(self.hash_vector(sentence.strip()))
        return embeddings

    def embed_query(self, query):
        # same as passage in stub
        return self.hash_vector(query.strip())

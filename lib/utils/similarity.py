from typing import Sequence
import math

def cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0

    dot_product = 0.0
    norm_a = 0.0
    norm_b = 0.0

    for x, y in zip(a, b):
        dot_product += x * y
        norm_a += x * x
        norm_b += y * y

    norm_product = math.sqrt(norm_a) * math.sqrt(norm_b)
    if norm_product == 0.0:
        return 0.0

    return float(dot_product / norm_product)

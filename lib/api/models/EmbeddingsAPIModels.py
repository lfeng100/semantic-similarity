from typing import List
from pydantic import BaseModel, field_validator

# https://docs.pydantic.dev/latest/api/functional_validators/#pydantic.functional_validators.field_validator
class EmbeddingsBulkRequest(BaseModel):
    sentences: List[str]

    @field_validator("sentences")
    @classmethod
    def check_sentence_list(cls, v):
        # check if each sentences field exists and is a list
        if not v or not isinstance(v, list):
            raise ValueError("sentences must be a non-empty list of strings")

        # check if each sentence is string and not empty
        for sentence in v:
            if not isinstance(sentence, str) or not sentence.strip():
                raise ValueError("each sentence must be a non-empty string")
        return v

class SimilarityRequest(BaseModel):
    sentence_1: str
    sentence_2: str

    @field_validator("sentence_1", "sentence_2")
    @classmethod
    def check_sentence(cls, v):
        # check if each sentence is string and not empty
        if not isinstance(v, str) or not v.strip():
            raise ValueError("each sentence must be a non-empty string")
        return v

class SearchRequest(BaseModel):
    query: str
    sentences: List[str]

    @field_validator("query")
    @classmethod
    def check_query(cls, v):
        # check if query is string and not empty
        if not isinstance(v, str) or not v.strip():
            raise ValueError("query must be a non-empty string")
        return v

    @field_validator("sentences")
    @classmethod
    def sentences_non_empty(cls, v):
        # check if each sentences field exists and is a list
        if not v or not isinstance(v, list):
            raise ValueError("sentences must be a non-empty list of strings")
            
        # check if each sentence is string and not empty
        for sentence in v:
            if not isinstance(sentence, str) or not sentence.strip():
                raise ValueError("each sentence must be a non-empty string")
        return v

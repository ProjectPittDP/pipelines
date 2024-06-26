"""
title: ADV Pipeline
author: asmith
date: 2024-06-06
version: 1.0
license: MIT
description: Weaviate RAG pipeline
requirements: requests, llama-index, llama-index-llms-ollama, llama-index-embeddings-ollama
"""

from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.weaviate import WeaviateVectorStore
import weaviate
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings
from llama_index.core import StorageContext
import requests

class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "pipeline_example"

        # The name of the pipeline.
        self.name = "ADV"
        pass

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        client = weaviate.connect_to_local("host.docker.internal","8080")

        # dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
        # docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in dataset]

        # documents = SimpleDirectoryReader("./data/").load_data()

        # config llm and embeddings
        Settings.llm = Ollama(model="llama3", request_timeout=120.0)

        Settings.embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            base_url="http://host.docker.internal:11434",
            # ollama_additional_kwargs={"mirostat": 0.1},
        )

        # This function is called when the server is started.
        global documents, index

        self.documents = SimpleDirectoryReader("./data").load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    async def on_valves_updated(self):
        # This function is called when the valves are updated.
        pass

    async def inlet(self, body: dict, user: dict) -> dict:
        # This function is called before the OpenAI API request is made. You can modify the form data before it is sent to the OpenAI API.

        print(body)
        print(user)

        return body

    async def outlet(self, body: dict, user: dict) -> dict:
        # This function is called after the OpenAI API response is completed. You can modify the messages after they are received from the OpenAI API.
        print(f"outlet:{__name__}")

        print(body)
        print(user)

        return body

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        # If you'd like to check for title generation, you can add the following check
        if body.get("title", False):
            print("Title Generation Request")

        # OLLAMA_BASE_URL = "http://host.docker.internal:11434"
        # MODEL = "llama3"

        # if "user" in body:
        #     print("######################################")
        #     print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
        #     print(f"# Message: {user_message}")
        #     print("######################################")

        # try:
        #     r = requests.post(
        #         url=f"{OLLAMA_BASE_URL}/v1/chat/completions",
        #         json={**body, "model": MODEL},
        #         stream=True,
        #     )

        #     r.raise_for_status()

        #     if body["stream"]:
        #         return r.iter_lines()
        #     else:
        #         return r.json()
        # except Exception as e:
        #     return f"Error: {e}"
        
        print(messages)
        print(user_message)

        query_engine = self.index.as_query_engine(streaming=True)
        response = query_engine.query(user_message)

        return response.response_gen
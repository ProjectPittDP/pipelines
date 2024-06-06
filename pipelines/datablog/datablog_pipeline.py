from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import requests
import os

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
        self.name = "Debevoise Data Blog"
        
        # Initialize rate limits
        self.valves = self.Valves()


    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
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
        print(f"inlet:{__name__}")

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

        # # If you'd like to check for title generation, you can add the following check
        # if body.get("title", False):
        #     print("Data Blog Chat")
        # else:
        #     titles = []
        #     for query in [user_message]:
        #         query = query.replace(" ", "_")

        #         r = requests.get(
        #             f"https://www.example.com/?s={query}"
        #         )

        #         response = r.json()
        #         titles = titles + response[1]
        #         print(titles)

        #     context = None
        #     if len(titles) > 0:
        #         r = requests.get(
        #             f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={'|'.join(titles)}"
        #         )
        #         response = r.json()
        #         # get extracts
        #         pages = response["query"]["pages"]
        #         for page in pages:
        #             if context == None:
        #                 context = pages[page]["extract"] + "\n"
        #             else:
        #                 context = context + pages[page]["extract"] + "\n"

        #     return context if context else "No information found"
        print(messages)
        print(user_message)
        print(body)

        return f"{__name__} response to: {user_message}"
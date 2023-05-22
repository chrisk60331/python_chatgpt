import re
from typing import List, Any

import openai

ENGINES = ("gpt-3.5-turbo",)


class OpenAIChat:
    def __init__(self, api_key: str):
        self.api_client = openai
        self.api_client.api_key = api_key

    def get_response(self, messages) -> List[Any]:
        responses = []

        for engine in ENGINES:
            try:
                response = self.api_client.ChatCompletion.create(
                    model=engine,
                    messages=messages,
                )

                for choice in response.choices:
                    responses.append((engine, choice.get("message")))

            except Exception as e:
                responses.append((engine, {"content": f"Error: {e}"}))

        return responses

    def label_code(self, snippet):
        prompt = (
            "can you provide one verb and one noun and one file extension of what this "
            f"code does in the format noun_verb.extension ? {snippet}"
        )
        message = {"role": "user", "content": prompt}
        response = self.get_response(
            messages=[message],
        )
        name = "_".join([r.get("content").strip() for _, r in response])
        return str().join(re.findall(r"^\S+_\S+\.\S+$", name)) or name

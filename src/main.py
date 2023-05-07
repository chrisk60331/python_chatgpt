import os
import threading
import queue
import time
from typing import Any, Dict, List
import logging

import openai
import spacy

nlp = spacy.load("en_core_web_sm")
API_KEY = os.environ.get("OPEN_AI_API_KEY")

class ChatThread(threading.Thread):
    def __init__(self, api_key: str, max_tokens: int = 50, temperature: float = 0.1):
        super().__init__(daemon=True)
        self.msg_queue = queue.Queue()
        self.max_tokens = max_tokens
        self.temperature = temperature
        openai.api_key = api_key
        self.api_client = openai
        self.history = []

    def get_response(self, engine: str, message: str) -> str:
        try:
            response = self.api_client.Completion.create(
                engine=engine,
                prompt=message,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                stop=None,
                timeout=30,
                logprobs=10
            )
            return response
        except Exception as e:
            return f"Error: {e}"

    def get_prompt(self, message: str) -> str:
        # Concatenate the relevant parts of the conversation history with the current message
        relevant_keywords =self.get_relevant_keywords(message)
        relevant_history = self.get_relevant_history(message, relevant_keywords)
        prompt = "\n".join(relevant_history + [message])
        return prompt

    def get_relevant_history(self, message: str, relevant_keywords: List[str]) -> List[str]:
        # Search for keywords or phrases in the conversation history that are related to the current message
        relevant_history = []
        for history_message in self.history:
            if " ".join(relevant_keywords) in history_message:
                relevant_history.append(history_message)
        return relevant_history

    def get_relevant_keywords(self, prompt: str) -> List[str]:
        doc = nlp(prompt)
        relevant_keywords = []
        for token in doc:
            if token.pos_ in ["NOUN", "VERB", "ADJ"] and not token.is_stop:
                relevant_keywords.append(token.text)
            elif token.ent_type_ != "" and not token.is_stop:
                relevant_keywords.append(token.text)
        return relevant_keywords

    def parse_response(self, response) -> str:
        parsed = {}
        if hasattr(response, "choices"):
            for choice in response.choices:
                logprobs = choice.get("logprobs").get("top_logprobs")
                for logprob in logprobs:
                    parsed["".join(logprob.keys())] = sum(logprob.values())

            return sorted(parsed, key=lambda x: parsed[x])[0]
        else:
            return response
    def run(self) -> None:
        engines =  ['davinci', 'curie', 'babbage', 'ada', 'curie-instruct-beta']
        while True:
            time.sleep(0.1)
            if not self.msg_queue.empty():
                message = self.msg_queue.get()
                self.history.append(message)
                prompt = self.get_prompt(message)

                for engine in engines:
                    response = self.parse_response(self.get_response(engine=engine, message=prompt))
                    print(f"ChatGPT[{engine}]: {response}")
            else:
                time.sleep(1)

    def send_message(self, msg: str) -> None:
        self.msg_queue.put(msg)


class ChatClient:
    def __init__(self, api_key: str) -> None:
        self.chat_thread = ChatThread(api_key)

    def start(self) -> None:
        self.chat_thread.start()
        while True:
            user_input = input("You: ")
            self.chat_thread.send_message(user_input)

if __name__ == "__main__":
    api_key = API_KEY
    chat_client = ChatClient(api_key)
    chat_client.start()

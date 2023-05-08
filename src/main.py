import os
import threading
import queue
import time
from typing import Any, List

import openai

API_KEY = os.environ.get("OPENAI_API_KEY", "")
ENGINES = ["gpt-3.5-turbo"]


class ChatThread(threading.Thread):
    def __init__(self, api_key: str):
        super().__init__(daemon=True)
        self.msg_queue: queue.Queue = queue.Queue()
        openai.api_key = api_key
        self.api_client = openai
        self.history: List[Any] = []

    def get_response(self, engine: str) -> List[Any]:
        try:
            response = self.api_client.ChatCompletion.create(
                model=engine,
                messages=self.history,
            )
            return [choice.get("message") for choice in response.choices]

        except Exception as e:
            return [f"Error: {e}"]

    def run(self) -> None:
        while True:
            time.sleep(0.1)
            if not self.msg_queue.empty():
                message = {"role": "user", "content": self.msg_queue.get()}
                self.history.append(message)

                for engine in ENGINES:
                    responses = self.get_response(engine=engine)
                    for response in responses:
                        print(f"ChatGPT[{engine}]: {response.get('content')}")
                        self.history.append(response)
            else:
                time.sleep(1)

    def send_message(self, msg: str) -> None:
        self.msg_queue.put(msg)


class ChatClient:
    def __init__(self, api_key: str) -> None:
        self.chat_thread = ChatThread(api_key)

    def start(self):
        print("Type '/exit' to end the conversation.")
        print("Type '/history' to show the conversation history.")
        self.chat_thread.start()
        while True:
            user_input = input("You: ")
            if user_input.lower() == "/exit":
                break
            elif user_input.lower() == "/history":
                self.print_history()
            else:
                self.chat_thread.send_message(user_input)

    def print_history(self):
        print("Conversation history:")
        for exchange in self.chat_thread.history:
            print(exchange)


if __name__ == "__main__":
    api_key = API_KEY
    chat_client = ChatClient(api_key)
    chat_client.start()

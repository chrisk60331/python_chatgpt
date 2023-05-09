import os
import threading
import queue
import time
from typing import Any, List

import tkinter as tk
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


class UserInput:
    def __init__(self):
        root = tk.Tk()
        self.message_input = tk.Text(root, height=10, width=30)
        self.message_input.pack()
        send_button = tk.Button(root, text="Send", command=self.send_message)
        send_button.pack(side="left", padx=(0, 10))
        cancel_button = tk.Button(root, text="Cancel", command=self.cancel_message)
        cancel_button.pack(side="right", padx=(10, 0))
        root.mainloop()

    def send_message(self):
        return self.message_input.get("1.0", "end-1c")

    def cancel_message(self):
        self.message_input.delete("1.0", "end")


class ChatClient:
    def __init__(self, api_key: str) -> None:
        self.chat_thread = ChatThread(api_key)

    def start(self):
        print("Type '/exit' to end the conversation.")
        print("Type '/history' to show the conversation history.")
        self.chat_thread.start()
        while True:
            user_input = UserInput()
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

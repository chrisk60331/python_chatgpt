import threading
import queue
from typing import Any, List
import logging

import time

from src.code_snippet import parse_code_snippets
from src.rate_limiter import RateLimiter
from src.text_to_speech import TextToSpeech
from src.audio_play import AudioPlayer

logging.basicConfig(level=logging.INFO)


class ChatThread(threading.Thread):
    def __init__(self, api_client):
        super().__init__(daemon=True)
        self.msg_queue: queue.Queue = queue.Queue()
        self.history: List[Any] = []
        self.api_client = api_client
        self.rate_limiter = RateLimiter()

    def send_message(self, msg: str) -> None:
        self.msg_queue.put(msg)

    def run(self) -> None:
        while True:
            if not self.msg_queue.empty():
                message = self.msg_queue.get()
                with self.rate_limiter:
                    responses = self.get_response(message)
                    self.handle_responses(responses)
            else:
                time.sleep(1)

    def handle_responses(self, responses):
        for engine, response in responses:
            self.history.append(response)
            response_content = response.get("content")
            print(f"ChatGPT [{engine}]: {response_content}")
            TextToSpeech().create_audio_file(response_content, "foo.mp3")
            AudioPlayer("foo.mp3").play()
            for snippet in parse_code_snippets(response_content):
                if isinstance(snippet, tuple):
                    snippet = "".join(snippet)
                with self.rate_limiter:
                    snippet.file_name = self.api_client.label_code(snippet)
                snippet.save()

    def get_response(self, message):
        message = {"role": "user", "content": message}
        self.history.append(message)
        return self.api_client.get_response(self.history)

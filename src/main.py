import os
import sys

from src.chat_client import ChatClient
from src.chat_thread import ChatThread
from src.openai_chat import OpenAIChat

API_KEY = os.environ.get("OPENAI_API_KEY", "")

if __name__ == "__main__":
    chat_thread = ChatThread(OpenAIChat(API_KEY))
    chat_client = ChatClient(chat_thread)
    if len(sys.argv) > 1:
        message = "\\s".join(sys.argv[1:])
        chat_thread.handle_responses(chat_thread.get_response(message))
    else:
        chat_client.start()

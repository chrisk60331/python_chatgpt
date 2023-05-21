import json

from src.user_input import UserInput


class ChatClient:
    def __init__(self, chat_thread):
        self.chat_thread = chat_thread

    def start(self):
        if not self.chat_thread._started._flag:
            self.chat_thread.start()

        while True:
            user_input = UserInput.multiline_input()
            if user_input.lower() == "/exit":
                break
            elif user_input.lower() == "/history":
                self.print_history()
            elif user_input.lower() == "/export":
                self.export_history()
            elif user_input.lower() == "/import":
                self.import_history()
            else:
                self.chat_thread.send_message(user_input)

    def print_history(self):
        print("Conversation history:")
        for exchange in self.chat_thread.history:
            print(exchange)

    def export_history(self, file_path: str = "conversation.json"):
        with open(file_path, "w") as f:
            f.write(json.dumps(self.chat_thread.history))

    def import_history(self, file_path: str = "conversation.json"):
        try:
            with open(file_path, "r") as f:
                self.chat_thread.history = json.loads(f.read())
        except Exception as e:
            print(e)

import unittest
from unittest.mock import patch, MagicMock
from queue import Queue

from src.main import ChatThread, ChatClient


class TestChatThread(unittest.TestCase):
    def setUp(self):
        self.api_key = "API_KEY"
        self.chat_thread = ChatThread(self.api_key)

    @patch("openai.Completion.create")
    def test_send_message(self, mock_completion):
        self.chat_thread.msg_queue = Queue()
        message = "Hello, ChatGPT!"
        self.chat_thread.send_message(message)
        self.assertEqual(self.chat_thread.msg_queue.get(), message)

    @patch("openai.Completion.create")
    def test_get_response(self, mock_completion):
        expected_response = "Hi there!"
        mock_completion.return_value.choices[0].text.strip.return_value = expected_response
        response = self.chat_thread.get_response("Hello, ChatGPT!")
        self.assertEqual(response, expected_response)

    @patch.object(ChatThread, "get_response", return_value="Hi there!")
    @patch("builtins.print")
    def test_run(self, mock_print, mock_get_response):
        self.chat_thread.msg_queue.put("Hello, ChatGPT!")
        self.chat_thread.run()
        mock_print.assert_called_with(f"ChatGPT: Hi there!")


class TestChatClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "API_KEY"
        self.chat_client = ChatClient(self.api_key)

    @patch("builtins.input", return_value="Hello, ChatGPT!")
    @patch.object(ChatThread, "send_message")
    @patch.object(ChatThread, "start")
    def test_start(self, mock_start, mock_send_message, mock_input):
        self.chat_client.start()
        mock_start.assert_called_once()
        mock_send_message.assert_called_once_with("Hello, ChatGPT!")


if __name__ == "__main__":
    unittest.main()

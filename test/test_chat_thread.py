import unittest
from unittest.mock import patch, Mock

import pytest

from src.chat_thread import ChatThread


class TestChatThread(unittest.TestCase):
    def __init__(self, method_name: str):
        super().__init__(method_name)
        mock_api = Mock()
        mock_api.get_response.return_value = [
            ("chat", {"content": "Hello, Chat thread"})
        ]
        self.chat_thread = ChatThread(mock_api)

    def test_send_message(self):
        message = "Hello, ChatGPT!"
        self.chat_thread.send_message(message)
        self.assertEqual(self.chat_thread.msg_queue.get(), message)

    @patch("builtins.print")
    def test_run(self, mock_print):
        self.chat_thread.msg_queue.put("Hello, ChatGPT!")
        with patch("src.chat_thread.time.sleep") as mock_time:
            mock_time.side_effect = StopIteration()
            with pytest.raises(StopIteration):
                self.chat_thread.run()
        mock_print.assert_called_with("ChatGPT [chat]: Hello, Chat thread")
